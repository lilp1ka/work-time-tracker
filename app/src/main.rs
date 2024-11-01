mod active_app;
mod afk;
mod config;
mod networking;
mod daemons{
    pub mod linux_daemonize;
}
use std::fs::{self, OpenOptions};
use active_app::{b_logs_from_file, b_logs_to_file, clear_file};
use active_app::{active_window, ActiveApp};
use afk::{is_afk, LastState};
use bincode::ErrorKind;
use device_query::{DeviceQuery, DeviceState};
use networking::{send_logs};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use std::time::{Duration, SystemTime};
use tokio::runtime::Runtime;
use tray_item::{TrayItem, IconSource};
use std::io::{Cursor, Read};
use std::fs::File;
use log::{info, warn, error, debug};

use std::io::{self};

use std::io::ErrorKind as IOErrorKind;

// use active_app::logs_from_file;
enum Message {
    OpenG,
    Quit,
    Update,
}

fn main() { 

    env_logger::init();
    info!("Logger initializated");
    if cfg!(target_os = "linux"){
        daemons::linux_daemonize::daemonize();
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
                
    let logger_handle = thread::spawn(move || loop { 
        let log_list_clone = Arc::clone(&log_list_clone2); 
        let rt_inner = rt_clone.lock().unwrap();

        let mut logs_to_send = {
            let mut log_list_inner = log_list_clone.lock().unwrap(); 
            if log_list_inner.len() < 3{
                drop(log_list_inner);
                continue;
            }
            let logs = log_list_inner.clone();
            log_list_inner.clear();
            logs
        };

        let logs_from_file = b_logs_from_file();

        if !logs_from_file.is_empty(){
            logs_to_send.extend(logs_from_file);
            debug!("[logs_to_send + logs_from_file] => {:#?}", logs_to_send);
        }
        let logs_copy = logs_to_send.clone();
        let send_result = rt_inner.block_on(async move{
            send_logs(logs_to_send).await
        });



        match send_result{
            Ok(response) => {
                info!("[send_result] response OK => {:#?}", response);
                let is_cleared = clear_file("/tmp/wtt-logs.bin");
                debug!("Is file logs-file cleared -> {:#?}", is_cleared);

                //вайпнуть потом,энивэй дебаг шляпа
                let content = match fs::read_to_string("/tmp/wtt-logs.bin"){
                    Ok(content) => content,
                    Err(ref e) if e.kind() == IOErrorKind::NotFound => {
                        error!("Not found /tmp/wtt-logs.bin file. Creating... ");
                        File::create("/tmp/wtt-logs.bin");
                        String::new()
                    },
                    Err(ref e) if e.kind() == IOErrorKind::PermissionDenied => {
                        error!("Permission Denied, please, change your /tmp/wtt-logs.bin file permissions \n [chmod 644]");
                        String::new()
                    },
                    Err(e) => {
                        error!("An unexcpected error ocured at logger_handle thread {e}");
                        String::new()
                    }
                };
                info!("FILE wtt-logs.bin cleared => {content}");
            },
            Err(err) => {
                debug!("Rewriting logs {:#?} to logs-file", logs_copy);
                b_logs_to_file(logs_copy);
                error!("[send_result] error => {:#?}", err);
                thread::sleep(Duration::from_secs(5));
            },
        }


        });

    let tray_thread = thread::spawn(move || {

    
        let cursor = Cursor::new(include_bytes!("icon.png"));
        let decoder = png::Decoder::new(cursor);
        let mut reader = decoder.read_info().unwrap();
        let info = reader.info().clone();
        let buff_size = info.width as usize * info.height as usize * 4 as usize;
        let mut buff = vec![0; buff_size];
        reader.next_frame(&mut buff);
    
        let icon = IconSource::Data {
            data: buff,
            height: info.height as i32, 
            width: info.width as i32,  
        };
    
        let mut tray = TrayItem::new("work-time-tracker", icon).unwrap();
    
        tray.add_label("example label").unwrap();
    
        let (tx, rx) = mpsc::sync_channel::<Message>(2);
    
        let update_tx = tx.clone();
        let quit_tx = tx.clone();
        let id_menu = tray
        .inner_mut()
        .add_menu_item_with_id("Open App", move ||{
            update_tx.send(Message::OpenG).unwrap()
        }).unwrap();
        tray.add_menu_item("Quit", move || {
            quit_tx.send(Message::Quit);
        });
        
        loop {
            match rx.recv(){
                Ok(Message::OpenG) => {
                    println!("openg");
                }
                Ok(Message::Quit) => {
                    println!("quit");
                    std::process::exit(0)
                }
                Ok(Message::Update) => {
                    println!("update");
                }
                Err(e) => {
                    println!("tray err: {}", e);
                } 
            }
        }
    
        
    });

    tray_thread.join().unwrap();
    active_window_handle.join().unwrap();
    is_afk_handle.join().unwrap();
    logger_handle.join().unwrap();

}



//если нету доступа к серверу логлист не обновляется
//хотя может и обновляется просто отсылает не обновленный


//короче сделал вроде пиздато с логами в бин но чета все равно только 3 отправляется я хз поч
//бля или логается ваще хуй пойми в пизду короче



//перенести короче нахуй запись в бин если нету ответа от сервера а не логать по кд в 
//бин и при этом держать в оперативе 