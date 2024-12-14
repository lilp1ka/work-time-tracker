use super::config::HOST_IP_ADDR;
use super::ActiveApp;
use reqwest::{Client, Error, Response};
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::{
    fmt::format, fs::OpenOptions, sync::{Arc, Mutex}
};
use std::io::Write;
use keyring::{Entry, Result as KResult};
use log::{info, warn, error, debug};
// pub fn logs_serialize(log_list: Vec<ActiveApp>) -> String {
//     let serialized = serde_json::to_string(&log_list).unwrap();
    
//     println!("==========================log_list: \n {:#?}", log_list);
//     serialized
// }

#[derive(Debug, Clone, Serialize, Deserialize)]
struct JwtToken{
    access_token: String,
    refresh_token: String
}


// fn get_jwt() -> Result<JwtToken, Error>{


// }

async fn request_jwt() -> Result<JwtToken, Error> {
    let creds = json!({
        "email": "kzr10820@inohm.com",
        "password": "sukasukasukasuka"
    }); // test creds

    let client = Client::new();
    let response = client
        .post(format!("{}/auth/login", HOST_IP_ADDR))
        .json(&creds)
        .send()
        .await?;

    if response.status().is_success() {
        let auth_response: JwtToken = response.json().await?;
        debug!("Deserialized response: {:?}", auth_response);
        Ok(auth_response)
    } else {
        error!("Authentication failed: HTTP {}", response.status());
        Err(response.error_for_status().unwrap_err())
    }
}




async fn refresh_jwt() -> Result<JwtToken, Error>{
    //test creds
    let refresh = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJrenIxMDgyMEBpbm9obS5jb20iLCJ1c2VybmFtZSI6Imh1ZXNvcyIsImVtYWlsX2lzX3ZlcmlmaWVkIjpmYWxzZSwiZXhwIjoxNzMzOTMyMDM0fQ.V8EzQlp-7H09Lc8QUfxCY63WaiuCof5rVJqY3SJ53ts";
    let client = Client::new();
    let json = json!({"refresh_token":refresh});
    let response = client
        .post(format!("{}/auth/login", HOST_IP_ADDR))
        .json(&json)
        .send()
        .await?;

    if response.status().is_success() {
        let auth_response: JwtToken = response.json().await?;
        debug!("Deserialized response: {:?}", auth_response);
        Ok(auth_response)
    } else {
        error!("Authentication failed: HTTP {}", response.status());
        Err(response.error_for_status().unwrap_err())
    }
}

pub async fn send_logs(log_list: Vec<ActiveApp>) -> Result<Response, Error> {
    let logs_json = json!({"log" : log_list} );

    // println!("TO SEND: {}", logs_json);

    let client = Client::new();

    let response = client
        .post(format!("{}/logs/", HOST_IP_ADDR))
        .json(&logs_json)
        .send()
        .await;
    // println!("RESPONSE: {:#?}", response);

    response
}


