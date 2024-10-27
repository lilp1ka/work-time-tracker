use super::afk::AfkMoment;
// use super::networking::logs_serialize;
use active_win_pos_rs::get_active_window;
use std::sync::{Arc, Mutex};
use thiserror::Error;
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
use bincode;
use serde_json::json;
use std::fs::{File, OpenOptions};

use std::io::{self, Read, Write};

pub fn active_window(app: Arc<Mutex<ActiveApp>>, log_list_n: Arc<Mutex<Vec<ActiveApp>>>) {
    let mut active_app = app.lock().unwrap();
    //temp
    let mut log_list = log_list_n.lock().unwrap();
    {
        match get_active_window() {
            Ok(window) => {
                if active_app.title != window.title {
                    active_app.duration = active_app.time.elapsed().unwrap();
                    log_list.push(active_app.clone());
                    
                    log_to_file(log_list.clone());

                    // drop(log_list);

                    // logs_serialize(log_list.clone()); //TEMP
                    //                                   // println!("LOG LIST ========================================================== \n {:#?}", log_list);
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


fn log_to_file(log_list: Vec<ActiveApp>) {
    let logs_json = serde_json::to_string_pretty(&log_list).unwrap();

    let mut file = OpenOptions::new()
        .write(true)
        .create(true)
        .append(true) 
        .open("/tmp/wtt-logzz.txt").unwrap();

    writeln!(file, "{}", logs_json).unwrap();

    file.flush().unwrap();
    
    println!("Data written to /tmp/wtt-logzz.txt");
}

pub fn logs_from_file() -> Result<Vec<ActiveApp>, FileLogErr>{
    let path = "/tmp/wtt-logzz.txt";
    let mut buf = String::new();
    let mut file = File::open(path).map_err(FileLogErr::OpenFile)?;

    file.read_to_string(&mut buf).map_err(FileLogErr::ReadFromFile)?;

    if buf.trim().is_empty(){
        return Err(FileLogErr::EmptyFile);
    } 
    println!("SUKA! {}", buf);
    let from_file_json: Vec<ActiveApp> = serde_json::from_str(&buf).map_err(FileLogErr::ParseToJson)?;
    println!("LOGS FROM FILE: {:#?}", from_file_json);
    Ok(from_file_json)
}


fn b_logs_from_file() -> io::Result<Vec<ActiveApp>>{
    let path = "/tmp/wtt-logs.bin"; 
    let mut file = OpenOptions::new().read(true).open(path)?;
    let mut buf: Vec<u8> = Vec::new();

    file.read_to_end(&mut buf)?;

    let logs: Vec<ActiveApp> = bincode::deserialize(&mut buf).unwrap(); //LATER error handle
    Ok(logs)

}

fn b_logs_to_file(mut logs: Vec<ActiveApp>) -> io::Result<()>{
    let path = "/tmp/wtt-logs.bin"; 

    let mut file = OpenOptions::new()
        .write(true)
        .create(true)
        .truncate(true) 
        .open(path)?;

    let logs_from_file = b_logs_from_file().unwrap();
    if !logs_from_file.is_empty(){
        logs.extend(logs_from_file);
    }
    let encoded: Vec<u8> = bincode::serialize(&logs).unwrap(); //LATER error handle

    file.write_all(&encoded);
    Ok(())
}


#[derive(Debug, Error)]
pub enum FileLogErr{
    #[error("Failed to open file")]
    ReadFromFile(#[source] std::io::Error),
    
    #[error("Failed read data to buffer")]
    OpenFile(#[source] std::io::Error),

    #[error("Failed to deserealize data from file: {0}")]
    ParseToJson(#[from] serde_json::Error),

    #[error("File is empty (no log data)")]
    EmptyFile
}
