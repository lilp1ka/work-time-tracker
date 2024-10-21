use super::afk::AfkMoment;
use super::networking::logs_serialize;
use active_win_pos_rs::get_active_window;
use std::sync::{Arc, Mutex};

use std::time::{Duration, SystemTime};

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ActiveApp {
    pub name: String,
    pub title: String,
    pub time: SystemTime,
    pub duration: Duration,
    pub is_afk: bool,
    pub afk_moments: Vec<AfkMoment>,
}

pub fn active_window(app: Arc<Mutex<ActiveApp>>, log_list_n: Arc<Mutex<Vec<ActiveApp>>>) {
    let active_app = app.lock().unwrap();
    //temp
    let mut log_list = log_list_n.lock().unwrap();
    {
        match get_active_window() {
            Ok(window) => {
                if active_app.title != window.title {
                    log_list.push(active_app.clone());

                    // drop(log_list);

                    logs_serialize(log_list.clone()); //TEMP
                                                      // println!("LOG LIST ========================================================== \n {:#?}", log_list);
                    drop(active_app);
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
