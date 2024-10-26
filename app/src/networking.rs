use super::config::HOST_IP_ADDR;
use super::ActiveApp;
use reqwest::{Client, Error, Response};
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::{
    fmt::format,
    sync::{Arc, Mutex},
};

pub fn logs_serialize(log_list: Vec<ActiveApp>) -> String {
    let serialized = serde_json::to_string(&log_list).unwrap();
    
    println!("==========================log_list: \n {:#?}", log_list);
    serialized
}

pub async fn send_logs(log_list: Vec<ActiveApp>) -> Result<Response, Error> {
    // let logs_serialized = logs_serialize(log_list);
    let logs_json = json!({"log" : log_list} );
    println!("TO SEND: {}", logs_json);
    // println!("LOGZ ZERIALIZED: {}", logs_serialized);

    let client = Client::new();

    let response = client
        .post(format!("{}/logs/", HOST_IP_ADDR))
        .json(&logs_json)
        .send()
        .await;
    println!("RESPONSE: {:#?}", response);

    response
}
