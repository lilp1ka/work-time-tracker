use active_win_pos_rs::get_active_window;
use device_query::{
    DeviceQuery, DeviceState, MousePosition,
};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, SystemTime};
fn main() {
    //device state & links
    let device_state = DeviceState::new();
    let last_state = Arc::new(Mutex::new(LastState {
        coords: device_state.get_mouse().coords,
        time: SystemTime::now(),
        duration: Duration::from_secs(0),
    }));
    let last_state_clone_is_afk = Arc::clone(&last_state); //for is_afk_handle
    let last_state_clone_active_window = Arc::clone(&last_state); //for active_window_handle

    //active app & links
    let now = SystemTime::now();
    let active_app = Arc::new(Mutex::new(ActiveApp {
        name: "None".to_string(),
        title: "None".to_string(),
        time: now,
        duration: Duration::from_secs(0),
    }));
    let active_app_clone = Arc::clone(&active_app); //for active_window_handle

    //log list & links
    let log_list: Vec<ActiveApp> = Vec::new();
    let log_list_clone = Arc::new(&log_list); 


    //threads
    let is_afk_handle = thread::spawn(move || loop {
        let last_state_inner = Arc::clone(&last_state_clone_is_afk);
        is_afk(last_state_inner);
        thread::sleep(Duration::from_millis(500));
    });

    let active_window_handle = thread::spawn(move || loop {
        let last_state_inner = Arc::clone(&last_state_clone_active_window);
        let active_app_inner = Arc::clone(&active_app_clone);
        active_window(active_app_inner, last_state_inner);
    });


    let logger_handle = thread::spawn(move || {});

    active_window_handle.join().unwrap();
    is_afk_handle.join().unwrap();

    //thread 1 (is afk):
    //monitoring device input
    //logs this into LastState
    //thread 2 (active window):
    //getting active window
    // if LastState.duration < 300s ? or log list longer then IDK
    //logs this into ActiveApp
    //else mark as afk
    //thread 3 (send logs):
    //sending logs every 5(?) mins

    //thread 1 uses:
    //last state arc mutex
    //thread 2 uses:
    //active window arc mutex
    //logs vec arc mutex (later)
    //thread 3 uses:
    //logs vec arc
    //last state arc (later)
}

#[derive(Debug)]
pub struct ActiveApp {
    name: String,
    title: String,
    time: SystemTime,
    duration: Duration,
}
#[derive(Debug)]
pub struct LastState {
    coords: MousePosition,
    time: SystemTime,
    duration: Duration,
}

fn is_afk(last_state: Arc<Mutex<LastState>>) {
    let device_state = DeviceState::new();
    let mut last_state = last_state.lock().unwrap();
    // loop {
    if !device_state.get_keys().is_empty()
        || device_state.get_mouse().coords != last_state.coords
        || device_state.get_mouse().button_pressed.contains(&true)
    {
        last_state.coords = device_state.get_mouse().coords;
        last_state.duration = last_state.time.elapsed().unwrap();
        last_state.time = SystemTime::now();
        println!(
            "{:#?} \n dur as sec: {}",
            last_state,
            last_state.duration.as_secs()
        );
    }
    thread::sleep(Duration::from_millis(500));
    // }
}

fn active_window(app: Arc<Mutex<ActiveApp>>, last_state: Arc<Mutex<LastState>>) {
    let active_app = app.lock().unwrap();

    {
        //loop
        match get_active_window() {
            Ok(window) => {
                if active_app.title != window.title {
                    println!(
                        "active_window: {:#?} {:?}",
                        active_app,
                        active_app.duration.as_secs()
                    );
                    let app_clone = Arc::clone(&app);
                    let last_state = Arc::clone(&last_state);
                    drop(active_app);
                    // log_active_app(app_clone, last_state);

                    let mut active_app = app.lock().unwrap();

                    active_app.name = window.app_name;
                    active_app.title = window.title;
                    active_app.time = SystemTime::now();
                }
            }
            Err(_) => {
                println!("errrr");
            }
        }
        thread::sleep(Duration::from_millis(500));
    }
}

fn log_active_app(
    app: Arc<Mutex<ActiveApp>>,
    last_state: Arc<Mutex<LastState>>,
    log_list: Arc<Mutex<Vec<ActiveApp>>>,
) {
    let mut app = app.lock().unwrap();
    let last_state = last_state.lock().unwrap();
    app.duration = app.time.elapsed().unwrap();
    // //dobavit' push v log list
    // if last_state.duration < 360{
    //     log_list.
    // }

    println!("LOGS: {:#?}, {}", app, app.duration.as_secs());
}
