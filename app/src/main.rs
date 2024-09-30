use x11::xlib::*;
use std::ffi::{CStr, CString};
use std::ptr;

fn main() {
    unsafe {
        let display = XOpenDisplay(ptr::null());
        if display.is_null() {
            panic!("Failed to connect to X Server");
        }

        let root = XDefaultRootWindow(display);
        let atom = XInternAtom(display, CString::new("_NET_ACTIVE_WINDOW").unwrap().as_ptr(), 0);

        let mut window: Window = 0;
        let mut actual_type = 0;
        let mut actual_format = 0;
        let mut nitems = 0;
        let mut bytes_after = 0;
        let mut prop: *mut u8 = ptr::null_mut();

        let status = XGetWindowProperty(
            display,
            root,
            atom,
            0,
            1,
            0,
            AnyPropertyType as u64,
            &mut actual_type,
            &mut actual_format,
            &mut nitems,
            &mut bytes_after,
            &mut prop,
        );

        if status != Success as i32 {
            println!("Failed to get status: {}", status);
        } else if nitems > 0 {
            window = *(prop as *mut Window);
            XFree(prop as *mut libc::c_void);
            println!("Got active window: {:?}", window);
        } else {
            println!("Couldn't find active window");
            XFree(prop as *mut libc::c_void);
            return;
        }


        let mut name: *mut i8 = ptr::null_mut();
        if XFetchName(display, window, &mut name) != 0 && !name.is_null() {
            let window_name = CStr::from_ptr(name).to_string_lossy().into_owned();
            XFree(name as *mut libc::c_void);
            println!("Active window name: {}", window_name);
        } else {
            println!("Didn't get active window name, checking other things...");

            let mut wm_name: *mut u8 = ptr::null_mut();
            let wm_atom = XInternAtom(display, CString::new("WM_NAME").unwrap().as_ptr(), 0);
            let status = XGetWindowProperty(
                display,
                window,
                wm_atom,
                0,
                100,
                0,
                AnyPropertyType.try_into().unwrap(),
                &mut actual_type,
                &mut actual_format,
                &mut nitems,
                &mut bytes_after,
                &mut wm_name,
            );

            if status == Success as i32 && nitems > 0 && !wm_name.is_null() {
                let wm_name_str = CStr::from_ptr(wm_name as *mut i8).to_string_lossy().into_owned();
                XFree(wm_name as *mut libc::c_void);
                println!("WM_NAME active window: {}", wm_name_str);
            } else {
                println!("couldnt get WM_NAME.");
            }
        }

        XCloseDisplay(display);
    }
}
