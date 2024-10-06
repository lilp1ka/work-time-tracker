mod afk;
mod active_app;
mod networking;
mod config;
use afk::{LastState, is_afk};
use active_app::{ActiveApp, active_window};
use device_query::{DeviceQuery, DeviceState};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, SystemTime};
use networking::{send_logs, logs_serialize};
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
    let log_list: Vec<ActiveApp> = Vec::new();
    let log_list_clone = Arc::new(Mutex::new((log_list)));

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

    let logger_handle = thread::spawn(move || loop{
        
    });

    active_window_handle.join().unwrap();
    is_afk_handle.join().unwrap();
    logger_handle.join().unwrap();
}


//networking.rs later
