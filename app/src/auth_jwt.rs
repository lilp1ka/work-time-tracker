use reqwest::{Client, Error as ReqwestError, Response};
use serde_json::json;
use std::{
    fmt::format, fs::OpenOptions, sync::{Arc, Mutex}
};
use std::io::Write;
use keyring::{error, Entry, Result as KResult};
use log::{info, warn, error, debug};
use serde::{Deserialize, Serialize};
use std::thread;
use thiserror::Error;
use std::io;
use std::io::BufRead;



pub const HOST_IP_ADDR: &str = "http://127.0.0.1:8001";



async fn request_jwt(login: &str, password: &str) -> Result<JwtToken, ReqwestError> {
    let creds = json!({
        "email": login,
        "password": password
    }); // test creds

    let client = Client::new();

    let response = client
        .post(format!("{}/auth/login", HOST_IP_ADDR))
        .json(&creds)
        .send()
        .await?; // add matching errors if server is unrechable

    debug!("request_jwt -> response: {:#?}", response);   

    if response.status().is_success() {
        let auth_response: JwtToken = response.json().await?;
        debug!("request_jwt -> Deserialized response: {:#?}", auth_response);

        //store token
        store_tokens_in_keyring(&auth_response.access_token, &auth_response.refresh_token);

        //test retriving token
        let (test_access, test_refresh) = retrieve_tokens_from_keyring().unwrap();
        debug!("request_jwt -> TEST TOKEN RETRIVING: \n access: {} \n refresh: {}", test_access, test_refresh);


        Ok(auth_response)
    } else {
        error!("Authentication failed: HTTP {}", response.status());
        Err(response.error_for_status().unwrap_err())
    }
}



async fn refresh_jwt() -> Result<JwtToken, JwtError> {
    match retrieve_tokens_from_keyring() {
        Ok((access_token, refresh_token)) => {
            let client = Client::new();
            let json = json!({"refresh_token": refresh_token});
            let response = client
                .post(format!("{}/auth/token/refresh", HOST_IP_ADDR))
                .header("Authorization", format!("Bearer {}", access_token))
                .json(&json)
                .send()
                .await;

            match response {
                Ok(resp) if resp.status().is_success() => {
                    let auth_response: JwtToken = resp.json().await.map_err(|_| JwtError::RequestError)?;
                    debug!("refresh_jwt -> Deserialized response: {:#?}", auth_response);
                    Ok(auth_response)
                },
                Ok(resp) => {
                    error!("refresh_jwt -> Authentication failed: HTTP {}", resp.status());
                    let (login,password) = tty_login().unwrap();
                    let auth_response = request_jwt(&login, &password).await.map_err(|_| JwtError::InvalidCredentials)?;
                    debug!("refresh_jwt -> expired -> request_jwt token: {:#?}", auth_response);
                    Ok(auth_response)
                },
                Err(e) => {
                    error!("refresh_jwt -> Request error: {:?}", e);
                    Err(JwtError::RequestError)
                },
            }
        },
        Err(_) => {
            debug!("refresh_jwt -> couldn't retrive refresh jwt token");
            Err(JwtError::RefreshTokenExpired)
        },
    }
}
#[derive(Debug, Clone, Serialize, Deserialize)]
struct JwtToken{
    access_token: String,
    refresh_token: String
}
 


// store_jwt.rs





fn store_tokens_in_keyring(access_token: &str, refresh_token: &str) -> Result<(), keyring::Error> {
    let access_entry = Entry::new("wtt_access", "user")?;
    let refresh_entry = Entry::new("wtt_refresh", "user")?;

    access_entry.set_password(access_token)?;
    refresh_entry.set_password(refresh_token)?;
    Ok(())
}

fn retrieve_tokens_from_keyring() -> Result<(String, String), keyring::Error> {
    let access_entry = Entry::new("wtt_access", "user")?;
    let refresh_entry = Entry::new("wtt_refresh", "user")?;

    let access_token = access_entry.get_password()?;
    let refresh_token = refresh_entry.get_password()?;

    Ok((access_token, refresh_token))
}


//console login

fn tty_login() -> io::Result<(String, String)> {
    let tty_path = "/dev/tty"; 
    let tty = OpenOptions::new().read(true).write(true).open(tty_path)?;

    let mut reader = io::BufReader::new(&tty);
    let mut writer = &tty;

    writeln!(writer, "Enter your email: ")?;
    writer.flush()?;

    let mut email = String::new();
    reader.read_line(&mut email)?;

    writeln!(writer, "Enter your password: ")?;
    writer.flush()?;

    let mut password = String::new();
    reader.read_line(&mut password)?;

    writeln!(writer, "Thank you!")?;
    writer.flush()?;

    println!("Email: {}", email.trim());
    println!("Password: {}", password.trim());

    Ok((email, password))
}

#[derive(Debug, Error)]
pub enum JwtError {
    #[error("Failed to retrieve tokens from keyring")]
    KeyringError,

    #[error("Refresh token has expired")]
    RefreshTokenExpired,

    #[error("Request error")]
    RequestError,

    #[error("Invalid credentials")]
    InvalidCredentials
}