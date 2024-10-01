use std::thread;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use active_win_pos_rs::{get_active_window, ActiveWindow};
use device_query::{device_events, DeviceEvents, DeviceQuery, DeviceState, KeyboardCallback, MousePosition};

fn main() {
    is_afk();
    //thread 1 (is afk):
        //monitoring device input
        //logs this into LastState
    //thread 2 (active window):
        //getting active window
        // if LastState.duration < 300s 
            //logs this into ActiveApp
        //else mark as afk
    //thread 3 (send logs):
        //sending logs every 5(?) mins
    
    //thread 1 uses:
        //last state arc mutex
    //thread 2 uses:
        //active window arc mutex
        //logs vec arc mutex
        //last state arc
    //thread 3 uses:
        //logs vec arc
}

#[derive (Debug)]
pub struct ActiveApp{
    name: String,
    title: String,
    time: SystemTime,
    duration: Duration
}
#[derive(Debug)]
pub struct LastState{
    coords: MousePosition,
    time: SystemTime,
    duration: Duration
}

fn is_afk(){
    let device_state = DeviceState::new();

    let mut last_state = LastState{
        coords: device_state.get_mouse().coords,
        time: SystemTime::now(),
        duration: Duration::from_secs(0),
    };
    loop{
            if !device_state.get_keys().is_empty() || 
                device_state.get_mouse().coords != last_state.coords || 
                device_state.get_mouse().button_pressed.contains(&true){
                    last_state.coords = device_state.get_mouse().coords;
                    last_state.duration = last_state.time.elapsed().unwrap();
                    last_state.time = SystemTime::now();
                    println!("{:#?} \n dur as sec: {}", last_state, last_state.duration.as_secs());
                }
            thread::sleep(Duration::from_millis(500));
        }
}

fn active_window(){
    let mut logs: Vec<ActiveApp> = Vec::new(); //potom vinesti v nachalo potoka
    let now = SystemTime::now(); //potom vinesti v nachalo potoka
    let mut active_app = ActiveApp{
                                    name: "None".to_string(),
                                    title: "None".to_string(),
                                    time: now,
                                    duration: Duration::from_secs(0)
                                    };
    
    println!("{:?}", now);
    loop{
        match get_active_window(){
            Ok(window) => {
                if active_app.name != window.app_name && active_app.title != window.title{
                    log_active_app(&mut active_app);

                    active_app.name = window.app_name;
                    active_app.title = window.title;
                    active_app.time = SystemTime::now();
                }
                else if active_app.title != window.title {
                    log_active_app(&mut active_app);

                    active_app.title = window.title;
                    active_app.time = SystemTime::now();
                }
                
            },
            Err(_) => {},
        }
        thread::sleep(Duration::from_millis(500));
    }
}

fn log_active_app(app: &mut ActiveApp){
    app.duration = app.time.elapsed().unwrap();
    //dobavit' push v log list
    println!("{:#?}, {}", app, app.duration.as_secs());

}
