use super::active_app::ActiveApp;
use device_query::{DeviceQuery, DeviceState, MousePosition};
use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};
use std::time::{Duration, SystemTime};

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
    //мб потом дописать если разница между афк моментами
    let device_state = DeviceState::new(); // 1 старттайм + 1 дуратион +-= 2 страттайм то стакать афк моментыч
    let mut last_state = last_state.lock().unwrap();
    let mut active_app = active_app.lock().unwrap();

    if !device_state.get_keys().is_empty()
        || device_state.get_mouse().coords != last_state.coords
        || device_state.get_mouse().button_pressed.contains(&true)
    {
        last_state.coords = device_state.get_mouse().coords;
        last_state.duration = last_state.time.elapsed().unwrap();
        last_state.time = SystemTime::now();
    } else {
        last_state.duration = last_state.time.elapsed().unwrap();

        if last_state.duration > Duration::from_secs(5) {
            if let Some(last_afk_moment) = active_app.afk_moments.last_mut() {
                //test  perviy li eto afk moment
                if !active_app.is_afk {
                    active_app.afk_moments.push(AfkMoment {
                        start_time: SystemTime::now() - last_state.duration,
                        duration: last_state.duration,
                    });
                    println!("AFK moment logged: {:?}", active_app.afk_moments);
                    active_app.is_afk = true
                } else {
                    active_app.afk_moments.last_mut().unwrap().duration = last_state.duration;
                    println!("AFK moment updated: {:?}", active_app.afk_moments);
                }
            } else {
                active_app.afk_moments.push(AfkMoment {
                    start_time: SystemTime::now() - last_state.duration,
                    duration: last_state.duration,
                });
                active_app.is_afk = true;
            }
        } else {
            active_app.is_afk = false
        }
    }
}
