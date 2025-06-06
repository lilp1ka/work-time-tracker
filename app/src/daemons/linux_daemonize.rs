
use std::fs::File;
use std::fs::remove_file;
use daemonize::{Daemonize, Group, User};
use uzers::{get_current_gid, get_current_groupname, get_current_uid, get_current_username};

use log::{info, warn, error, debug};

pub fn daemonize(){
    if cfg!(target_os = "linux"){
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

}