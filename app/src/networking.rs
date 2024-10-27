use super::config::HOST_IP_ADDR;
use super::ActiveApp;
use reqwest::{Client, Error, Response};
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::{
    fmt::format, fs::OpenOptions, sync::{Arc, Mutex}
};
use std::io::Write;

// pub fn logs_serialize(log_list: Vec<ActiveApp>) -> String {
//     let serialized = serde_json::to_string(&log_list).unwrap();
    
//     println!("==========================log_list: \n {:#?}", log_list);
//     serialized
// }

pub async fn send_logs(log_list: Vec<ActiveApp>) -> Result<Response, Error> {
    let logs_json = json!({"log" : log_list} );

    println!("TO SEND: {}", logs_json);

    let client = Client::new();

    let response = client
        .post(format!("{}/logs/", HOST_IP_ADDR))
        .json(&logs_json)
        .send()
        .await;
    println!("RESPONSE: {:#?}", response);

    response
}



//логи с оперативы беру,если тхт не пустой,мерджу,отправляю
//если не отправляется переписываю нахуй всё в тхт
//если отправляется вайпаю тхт
//
//
//
//