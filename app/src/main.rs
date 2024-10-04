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
        name: "None".to_string(), //maybe get real active app 
        title: "None".to_string(),
        time: now,
        duration: Duration::from_secs(0),
        afk_moments: Vec::new() // ETO POTOM UBRAT NAHUI
    }));
    let active_app_clone = Arc::clone(&active_app); //for active_window_handle
    let active_app_clone_is_afk = Arc::clone(&active_app); //for is_afk
    //log list & links
    let mut log_list: Vec<ActiveApp> = Vec::new();
    let log_list_clone = Arc::new(Mutex::new((log_list)));



    //threads
    let is_afk_handle = thread::spawn(move || loop {
        let last_state_inner = Arc::clone(&last_state_clone_is_afk);
        let active_app_inner =  Arc::clone(&active_app_clone_is_afk);
        is_afk(last_state_inner, active_app_inner);
        thread::sleep(Duration::from_millis(50));
    });

    let active_window_handle = thread::spawn(move || loop {
        let last_state_inner = Arc::clone(&last_state_clone_active_window);
        let active_app_inner = Arc::clone(&active_app_clone);
        let log_list_inner = Arc::clone(&log_list_clone);
        active_window(active_app_inner, last_state_inner, log_list_inner);
        thread::sleep(Duration::from_millis(500));        
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

#[derive(Debug, Clone)]
pub struct ActiveApp {
    name: String,
    title: String,
    time: SystemTime,
    duration: Duration,
    afk_moments: Vec<AfkMoment>
}

#[derive(Debug, Clone)]
pub struct AfkMoment{
    start_time: SystemTime,
    duration: Duration
}

#[derive(Debug)]
pub struct LastState {
    coords: MousePosition,
    time: SystemTime,
    duration: Duration,
}

fn is_afk(last_state: Arc<Mutex<LastState>>, active_app: Arc<Mutex<ActiveApp>>){
    let device_state = DeviceState::new();
    let mut last_state = last_state.lock().unwrap();
    let mut active_app = active_app.lock().unwrap();
    // loop {
    

    if !device_state.get_keys().is_empty()
        || device_state.get_mouse().coords != last_state.coords
        || device_state.get_mouse().button_pressed.contains(&true)
    {
        last_state.coords = device_state.get_mouse().coords;
        last_state.duration = last_state.time.elapsed().unwrap();
        last_state.time = SystemTime::now();
    }
    else {
        last_state.duration = last_state.time.elapsed().unwrap();
        
        if last_state.duration > Duration::from_secs(300) {
            active_app.afk_moments.push(AfkMoment {
                start_time: SystemTime::now() - last_state.duration, 
                duration: last_state.duration,
            });
            println!("AFK moment logged: {:?}", active_app.afk_moments.last());
        }
    }
}

fn active_window(app: Arc<Mutex<ActiveApp>>,
                 last_state: Arc<Mutex<LastState>>,
                 log_list: Arc<Mutex<Vec<ActiveApp>>>) {
    let active_app = app.lock().unwrap();
    // let last_state = Arc::clone(&last_state);
    {
        //loop
        match get_active_window() {
            Ok(window) => {
                if active_app.title != window.title {
                    // println!(
                    //     "active_window: {:#?} {:?}",
                    //     active_app,
                    //     active_app.duration.as_secs()
                    // );
                    let app_clone = Arc::clone(&app);
                    //get result is afk
                    drop(active_app);
                    // log_active_app(app_clone, last_state, log_list);

                    let mut active_app = app.lock().unwrap();

                    active_app.name = window.app_name;
                    active_app.title = window.title;
                    active_app.time = SystemTime::now();
                    println!("REALACTIVEAPP: {}", active_app.title);
                }

                
            }
            Err(_) => {
                println!("errrr");
            }
        }
    }
}

fn log_active_app(
    app: Arc<Mutex<ActiveApp>>,
    last_state: Arc<Mutex<LastState>>,
    log_list: Arc<Mutex<Vec<ActiveApp>>>,
) {
    let mut app = app.lock().unwrap();
    let last_state = last_state.lock().unwrap();
    let mut log_list = log_list.lock().unwrap();
    app.duration = app.time.elapsed().unwrap();
    // //dobavit' push v log list
    if last_state.duration > Duration::from_secs(5){
        log_list.push(ActiveApp {
                        name: "AFK".to_string(),
                        title: "AFK".to_string(),
                        time: app.time,
                        duration: app.duration,
                        afk_moments: Vec::new() //ETO TEMPORARY HUETA
                    });
        println!("LOG LIST: {:#?}", log_list);
    }
    else if last_state.duration <= Duration::from_secs(5){ // !!!!!!!! CHANGE DURATION LATER
        log_list.push(app.clone());
        println!("LOG LIST: \n{:#?}", log_list);
    }
    // println!("LOGS: {:#?}, {}", app, app.duration.as_secs());
}

//ошибка в логике кода
//я сначала логирую ласт мув
//потом если он меньше 5 то сохраняю как работу а не афк
//нужно сначала 
//
//я вызываю из афк только на измeнении окна
//а надо вызывать постоянно
//но как мне так слепить бы две этих функции что бы они не накладывались
//
//
//
//если меняется окно то значит был мув
//получается нужно брать предпоследений мув а не тока шо который
//
//
//
//
//
//
//
//
//
//
//
//
//
