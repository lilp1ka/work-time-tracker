use super::active_app::ActiveApp;
use device_query::{DeviceQuery, DeviceState, MousePosition};
use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};
use std::time::{Duration, SystemTime};

use log::{info, warn, error, debug};
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AfkMoment {
    start_time: SystemTime,
    duration: Duration,
}

#[derive(Debug)]
pub struct LastState {
    pub coords: MousePosition,
    pub time: SystemTime,
    pub duration: Duration,
}

pub fn is_afk(last_state: Arc<Mutex<LastState>>, active_app: Arc<Mutex<ActiveApp>>) {
    let device_state = DeviceState::new(); 
    let mut last_state = last_state.lock().unwrap();
    let mut active_app = active_app.lock().unwrap();

    if !device_state.get_keys().is_empty()
        || device_state.get_mouse().coords != last_state.coords
        || device_state.get_mouse().button_pressed.contains(&true)
    {
        last_state.coords = device_state.get_mouse().coords;
        last_state.duration = last_state.time.elapsed().unwrap();
        last_state.time = SystemTime::now();

        if active_app.is_afk {
            active_app.is_afk = false; 
        }
    } else {
        last_state.duration = last_state.time.elapsed().unwrap();

        if last_state.duration > Duration::from_secs(5) {
            if !active_app.is_afk {
                active_app.afk_moments.push(AfkMoment {
                    start_time: SystemTime::now() - last_state.duration,
                    duration: last_state.duration,
                });
                info!("AFK moment logged");
                active_app.is_afk = true
            } else {
                active_app.afk_moments.last_mut().unwrap().duration = last_state.duration;
                info!("AFK moment updated");
            }
        }
         else {
            active_app.is_afk = false;
        }
    }
}

//поле is_afk в структуре ActiveApp отвечает за состояние в данный момент
//что бы понимать,новый афк момент создавать или апдейтить старый