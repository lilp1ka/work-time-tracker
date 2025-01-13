import axios from "axios"
const BACKEND_DOMAIN = "http://127.0.0.1:8001/";

const REGISTER_URL = `${BACKEND_DOMAIN}auth/register`;
const LOGIN_URL = `${BACKEND_DOMAIN}auth/login`;
const LOGOUT_URL = `${BACKEND_DOMAIN}auth/logout`;


const register = async (userData) => {
    const config = {
        headers: {
            "Content-type": "application/json"
        }
    };
    const response = await axios.post(REGISTER_URL, userData, config);
    return response.data;
};

const login = async (userData) => {
    const config = {
        headers: {
            "Content-type": "application/json"
        }
    };
    try {
        const response = await axios.post(LOGIN_URL, userData, config);
        
        // При успішному логіні зберігаємо токен
        if (response.data && response.data.access_token) {
            localStorage.setItem("token", response.data.access_token);
        }

        return response.data;
    } catch (error) {
        console.error("Login failed:", error);
        throw error;
    }
};

const logout = async () => {
    try {
        const config = {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`,
                "Content-type": "application/json"
            }
        };
        await axios.post(LOGOUT_URL, {}, config);
        localStorage.removeItem("token");
    } catch (error) {
        console.error("Logout failed:", error);
        throw error;
    }
};

const getTokenFromLocalStorage = () => {
    return localStorage.getItem("token");
};

const authService = { register, login, logout, getTokenFromLocalStorage}

export default authService