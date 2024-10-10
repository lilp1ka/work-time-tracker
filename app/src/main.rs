mod active_app;
mod afk;
mod config;
mod networking;
use active_app::{active_window, ActiveApp};
use afk::{is_afk, LastState};
use device_query::{DeviceQuery, DeviceState};
use networking::{logs_serialize, send_logs};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, SystemTime};
use tokio::runtime::Runtime;

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
        afk_moments: Vec::new(), // ETO POTOM UBRAT NAHUI
        is_afk: false,
    }));

    
    let active_app_clone = Arc::clone(&active_app); //for active_window_handle
    let active_app_clone_is_afk = Arc::clone(&active_app); //for is_afk
    
    //log list & links
    let log_list: Arc<Mutex<Vec<ActiveApp>>> = Arc::new(Mutex::new(Vec::new()));
    let log_list_clone = Arc::clone(&log_list);
    let log_list_clone2 = Arc::clone(&log_list);

    //runtime
    let rt = Arc::new(Mutex::new(Runtime::new().unwrap()));
    let rt_clone = Arc::clone(&rt);

    //threads
    let is_afk_handle = thread::spawn(move || loop {
        let last_state_inner = Arc::clone(&last_state_clone_is_afk);
        let active_app_inner = Arc::clone(&active_app_clone_is_afk);
        is_afk(last_state_inner, active_app_inner);
        thread::sleep(Duration::from_millis(500));
    });

    let active_window_handle = thread::spawn(move || loop {
        let active_app_inner = Arc::clone(&active_app_clone);
        let log_list_inner = Arc::clone(&log_list_clone);
        active_window(active_app_inner, log_list_inner);
        thread::sleep(Duration::from_millis(500));
    });

    let logger_handle = thread::spawn(move || loop {
        let log_list_clone = Arc::clone(&log_list_clone2);
        let mut log_list_inner =  log_list_clone.lock().unwrap();
        let rt_inner = rt_clone.lock().unwrap();
        if log_list_inner.len() >= 2 {
            let logs_to_send = log_list_inner.clone();
            rt_inner.block_on(async move{
                match send_logs(logs_to_send).await{
                    Ok(response) => {
                        println!("GOT RESPONSE {:#?}", response);
                        log_list_inner.clear();
                },
                    Err(err) => {eprintln!("Error {}", err);}
                }
            });
        }
    });

    active_window_handle.join().unwrap();
    is_afk_handle.join().unwrap();
    logger_handle.join().unwrap();
}

