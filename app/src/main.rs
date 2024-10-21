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

use daemonize::{Daemonize, Group, User};
use uzers::{get_current_gid, get_current_groupname, get_current_uid, get_current_username};


use std::fs::File;
use std::fs::remove_file;

fn main() { 


    // [linux] run with sudo only, cuz otherwise daemonize can't read pid file
    if cfg!(target_os = "linux"){
        // let user = env::var("USER").unwrap_or_else(|_| );
        println!("URA ETO LINUX");
        let stdout = match File::open("/tmp/wtt-daemon.out"){ // LATER clean after successful log send
        Ok(file) => {file},
        Err(_) => {
            File::create("/tmp/wtt-daemon.out").unwrap()},
    };

    let stderr = match File::open("/tmp/wtt-daemon.err"){ //LATER clean after successful log send
        Ok(file) => {file},
        Err(_) => {
            File::create("/tmp/wtt-daemon.err").unwrap()},
    };

    let pid_file_path = "/tmp/wtt-test.pid";

    let _ = remove_file(pid_file_path);

    let uid = get_current_uid();
    let gid = get_current_gid();

    //test
    let groupname = get_current_groupname().unwrap();
    let username = get_current_username().unwrap();
    println!("USER {:#?}, GROUP {:#?}", groupname, username);
    println!("USER {:#?}, GROUP {:#?}", uid, gid);
    let user: User = User::from(uid); 
    let group = Group::from(gid);
    println!("USER {:#?}, GROUP {:#?}", user, group);
    let daemonize = Daemonize::new()
        .pid_file("/tmp/wtt-test.pid") // Every method except `new` and `start`
        .chown_pid_file(false)      // is optional, see `Daemonize` documentation
        .working_directory("/tmp") // for default behaviour.
        .user(user)
        .group(group) // Group name        // or group id.
        .umask(0o777)    // Set umask, `0o027` by default.
        .stdout(stdout)  // Redirect stdout to `/tmp/daemon.out`.
        .stderr(stderr);  // Redirect stderr to `/tmp/daemon.err`.

    match daemonize.start() {
        Ok(_) => println!("Success, daemonized"),
        Err(e) => eprintln!("Error, {}", e),
    }

    }


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
                
    let logger_handle = thread::spawn(move || loop { // FIX тут пофиксить потому шо пиздец хуйня какая то все зависит от цифры 
        let log_list_clone = Arc::clone(&log_list_clone2); // на 2 строчки ниже. походу передается в асинк рт и все пиздец 
        let mut log_list_inner = log_list_clone.lock().unwrap(); //там зависает нахуй и финита ля комедиа (хинт; посмотреть арки в токио как юзать и припиздошить)
        let rt_inner = rt_clone.lock().unwrap();
        if log_list_inner.len() >= 3 {

            let logs_to_send = log_list_inner.clone();


            let send_result = rt_inner.block_on(async move{
                send_logs(logs_to_send).await
            });

            match send_result{
                Ok(response) => {
                    println!("GOT RESPONSE {:#?}", response);
                    log_list_inner.clear();
                    println!("[DEBUG] CLEAR VECTOR");
                    println!("[DEBUG] {:#?}", log_list_inner);
                    // вместо этой хуйни добавить мпск колл в хуйзнаеткуда бля короче
                }//что бы логи почистились по колу,и нужно что бы хуйзнаеткуда было не асинхронное,шоб не блочило поток,иначе пиздец
                Err(err) => {
                    eprintln!("GOT ERROR {}", err);
                    thread::sleep(Duration::from_secs(5));
                }
            }
        }
    });

    active_window_handle.join().unwrap();
    is_afk_handle.join().unwrap();
    logger_handle.join().unwrap();
}


//короче проблема с настройкой привелегий, то пид файл не открывается то еще чета.
//скорее всего буду запускать по дефолту от юзера. оставляю в рабочей версии все пока что
//таска: либо решить все таки чета с привелегиями либо прописать парс актив юзера + его группы 
//что бы под ним демон воркал
//
//
//
//
//
//
