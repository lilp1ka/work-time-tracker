use serde::{Serialize, Deserialize};
use serde_json::json;
use super::ActiveApp;
use std::{fmt::format, sync::{Arc, Mutex}};
use reqwest::Client;
use super::config::HOST_IP_ADDR;

pub fn logs_serialize(log_list: Arc<Mutex<Vec<ActiveApp>>>){
    let log_list = log_list.lock().unwrap();
    let serialized = serde_json::to_string(&*log_list.clone()).unwrap();
    send_logs(serialized);
}

pub async fn send_logs(log_list: String){
    let logs_json = json!({"log" : log_list} );
    println!("TO SEND: {}", logs_json);

    let client = Client::new();

    let response = client.post(format!("{}/logs/", HOST_IP_ADDR))
    .json(&logs_json)
    .send()
    .await;
    println!("RESPONSE: {:#?}", response);

}


