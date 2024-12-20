use keyring::{Entry, Error as KeyringError};
use log::{debug, error, info, warn};
use reqwest::Client;
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::thread;

use thiserror::Error;

use tokio::runtime::Runtime;

use clap::{Arg, Command as clCommand};
use std::process::{Command, Stdio};


pub const HOST_IP_ADDR: &str = "http://127.0.0.1:8001";

#[derive(Debug, Error)]
pub enum JwtError {
    #[error("Failed to retrieve tokens from keyring")]
    KeyringError,

    #[error("Refresh token has expired")]
    RefreshTokenExpired,

    #[error("Request error")]
    RequestError,

    #[error("Invalid credentials")]
    InvalidCredentials,

    #[error("Unexptected")]
    Unexptected,

    #[error("ConntectionError")]
    ConntectionError,

    #[error("KeyringFailure")]
    KeyringFailure,
}

fn main() {
    env_logger::init();

    let matches = clCommand::new("Auth Program")
        .version("1.0")
        .author("Author Name")
        .about("Authenticates to a server with login and password")
        .arg(
            Arg::new("login")
                .short('l')
                .long("login")
                .value_name("LOGIN")
                .help("Specifies the login")
                .required(false),
        ) // Этот аргумент должен быть предоставлен
        .arg(
            Arg::new("password")
                .short('p')
                .long("password")
                .value_name("PASSWORD")
                .help("Specifies the password")
                .required(false),
        ) // Этот аргумент должен быть предоставлен
        .get_matches();

    let test_handle = thread::spawn(move || {
        let rt = Runtime::new().expect("Failed to create Tokio runtime");

        if matches.contains_id("login") && matches.contains_id("password") {
            let login = matches
                .get_one::<String>("login")
                .expect("Username required");
            let password = matches
                .get_one::<String>("password")
                .expect("Password required");

            debug!("GOT CREDS FROM FLAGS: {:#?} {:#?}", login, password);

            rt.block_on(async {
                let (access_token, refresh_token) = match request_jwt(login, password).await{
                    Ok(JwtToken{access_token, refresh_token}) => {
                        store_tokens_in_keyring("wtt", &access_token, &refresh_token);
                        store_credentials_in_keyring("wtt", &login, &password);
                        (access_token, refresh_token)},

                    Err(JwtError::ConntectionError) => {
                        error!("Connection refused, check your internet connection.");
                        error!("App will work locally. To connect to the server kill PID and then enter correct creds.");
                        return;
                    }

                    Err(JwtError::InvalidCredentials) => {
                        error!("Invalid credentials");
                        error!("App will work locally. To connect to the server kill PID and then enter correct creds.");
                        return;
                    }

                    Err(_) => {
                        error!("Unexpected error");
                        return;
                    }
                };
            });
        } else {

            rt.block_on(async {
                match refresh_jwt().await{
                    Ok(JwtToken { access_token, refresh_token }) => {
                        debug!("refresh_jwt -> access: {}, refresh: {}", access_token, refresh_token);
                        match store_tokens_in_keyring("wtt", access_token.as_str(), refresh_token.as_str()){
                            Ok(_) => {
                                debug!("Tokens stored in keyring");
                                return;
                            }
                            Err(_) => {
                                error!("Couldn't save JWT tokens to keyring.");    
                                error!("App will work locally. To connect to the server kill PID and then enter correct creds.");
                                return;
                            } 
                        }
                    }

                    Err(JwtError::ConntectionError) => {
                        error!("Connection refused, check your internet connection.");
                        error!("App will work locally. To connect to the server kill PID and then enter correct creds.");
                        return;
                    }

                    Err(JwtError::InvalidCredentials) => {
                        
                        error!("Invalid credentials");
                        error!("App will work locally. To connect to the server kill PID and then enter correct creds.");
                        return;
                    }

                    Err(_) => {
                        error!("Unexpected error");
                        return;
                    }
                }
            });
        }


    });
    debug!("test_handle about to end");
    test_handle.join().expect("exit test_handle with code 1");
    debug!("test_handle ended");
}

pub async fn request_jwt(login: &str, password: &str) -> Result<JwtToken, JwtError> {
    
    let creds = json!({
        "email": login,
        "password": password
    }); 

    let client = Client::new();

    let response = client
        .post(format!("{}/auth/login", HOST_IP_ADDR))
        .json(&creds)
        .send()
        .await
        .map_err(|e| JwtError::ConntectionError)?; // add matching errors if server is unrechable

    debug!("request_jwt -> response: {:#?}", response);

    if response.status().is_success() {
        let auth_response: JwtToken = response.json().await.map_err(|e| JwtError::Unexptected)?;
        debug!("request_jwt -> Deserialized response: {:#?}", auth_response);

        //store token
        store_tokens_in_keyring(
            "wtt",
            &auth_response.access_token,
            &auth_response.refresh_token,
        );

        //test retriving token
        let (test_access, test_refresh) = match retrieve_tokens_from_keyring("wtt") {
            Ok(tokens) => tokens, 
            Err(e) => {
                error!("Failed to retrieve tokens from keyring: {:?}", e);
                return Err(JwtError::KeyringFailure);
            }
        };
        debug!(
            "request_jwt -> TEST TOKEN RETRIVING: \n access: {} \n refresh: {}",
            test_access, test_refresh
        );

        Ok(auth_response)
    } else {
        error!("Authentication failed: HTTP {}", response.status());
        Err(JwtError::InvalidCredentials)
    }
}

pub async fn refresh_jwt() -> Result<JwtToken, JwtError> {
    match retrieve_tokens_from_keyring("wtt") {
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
                    let auth_response: JwtToken =
                        resp.json().await.map_err(|_| JwtError::Unexptected)?;
                    debug!("refresh_jwt -> Deserialized response: {:#?}", auth_response);
                    store_tokens_in_keyring("wtt", &auth_response.access_token, &auth_response.refresh_token);
                    Ok(auth_response)
                }

                Ok(resp) if resp.status().is_client_error() => match request_token_with_creds().await{
                    Ok(JwtToken { access_token, refresh_token }) => {
                        debug!("req_token_w_creds -> access: {}, refresh: {}", access_token, refresh_token);
                        match store_tokens_in_keyring("wtt", access_token.as_str(), refresh_token.as_str()){
                            Ok(_) => {
                                debug!("creds stored into a keyring");
                                Ok(JwtToken { access_token: access_token, refresh_token: refresh_token })
                            }
                            Err(_) => {
                                error!("Invalid credentials");
                                error!("App will work locally. To connect to the server kill PID and then enter correct creds.");
                                Err(JwtError::KeyringError)}
                        }
                    }
                    Err(_) => Err(JwtError::InvalidCredentials)
                },

                Ok(_) => Err(JwtError::Unexptected),

                Err(_) => Err(JwtError::ConntectionError),
            }
        }
        Err(_) => Err(JwtError::KeyringError),
    }
}

pub async fn request_token_with_creds() -> Result<JwtToken, JwtError> {
    match retrieve_credentials_from_keyring("wtt") {
        Ok((login, password)) => match request_jwt(&login, &password).await {
            Ok(auth_response) => Ok(auth_response),
            Err(_) => Err(JwtError::InvalidCredentials),
        },
        Err(_) => Err(JwtError::InvalidCredentials),
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JwtToken {
    pub access_token: String,
    pub refresh_token: String,
}


pub fn store_credentials_in_keyring(
    service: &str,
    username: &str,
    password: &str,
) -> Result<(), KeyringError> {
    let username_entry = Entry::new(&format!("{}_username", service), "user")?;
    let password_entry = Entry::new(&format!("{}_password", service), "user")?;

    username_entry.set_password(username)?;
    password_entry.set_password(password)?;
    Ok(())
}

pub fn retrieve_credentials_from_keyring(service: &str) -> Result<(String, String), KeyringError> {
    let username_entry = Entry::new(&format!("{}_username", service), "user")?;
    let password_entry = Entry::new(&format!("{}_password", service), "user")?;

    let username = username_entry.get_password()?;
    let password = password_entry.get_password()?;

    Ok((username, password))
}

pub fn store_tokens_in_keyring(
    service: &str,
    access_token: &str,
    refresh_token: &str,
) -> Result<(), KeyringError> {
    let access_entry = Entry::new(&format!("{}_access", service), "user")?;
    let refresh_entry = Entry::new(&format!("{}_refresh", service), "user")?;

    access_entry.set_password(access_token)?;
    refresh_entry.set_password(refresh_token)?;
    Ok(())
}

pub fn retrieve_tokens_from_keyring(service: &str) -> Result<(String, String), KeyringError> {
    let access_entry = Entry::new(&format!("{}_access", service), "user")?;
    let refresh_entry = Entry::new(&format!("{}_refresh", service), "user")?;

    let access_token = access_entry.get_password()?;
    let refresh_token = refresh_entry.get_password()?;

    Ok((access_token, refresh_token))
}

pub fn handle_credentials_flow() -> (String, String) {
    let login = request_credentials("Enter your email:").expect("Failed to read email");
    let password = request_credentials("Enter your password:").expect("Failed to read password");
    (login, password)
}

pub fn request_credentials(prompt: &str) -> Result<String, std::io::Error> {
    let output = Command::new("systemd-ask-password")
        .arg(prompt)
        .stdin(Stdio::inherit())
        .stdout(Stdio::piped())
        .stderr(Stdio::inherit())
        .output()?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).trim().to_string())
    } else {
        Err(std::io::Error::new(
            std::io::ErrorKind::Other,
            "Failed to get credentials",
        ))
    }
}
