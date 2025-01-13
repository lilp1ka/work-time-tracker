import React, { createContext, useContext, useState, useCallback, useEffect } from "react";
import axios from "axios";


const API_BASE_URL = "http://127.0.0.1:8001/";
const GlobalContext = React.createContext();

export const ContextProvider = ({ children }) => {
  const [users, setUsers] = useState([]); // Для зберігання всіх користувачів
  const [currentUser, setCurrentUser] = useState(null); // Для зберігання поточного користувача
  const [loading, setLoading] = useState(false); // Стан завантаження
  const [error, setError] = useState(null); // Для обробки помилок
  const token = localStorage.getItem("token");
  
  useEffect(() => {
    if (!token) {
      setError("User is not authenticated.");
      setLoading(false);
      return;
    }
    // Отримуємо поточного користувача після перевірки токена
    getCurrentUser();
  }, [token]); // Запуск тільки при зміні token


  // Отримати всіх користувачів
  const getAllUsers = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}users/get-all-users`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUsers(response.data);
    } catch (err) {
      setError(err.message);
      console.error("Error fetching all users:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Отримати користувача за ID
  const getUserById = async (userId) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}users/get-user-by-id`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: { user_id: userId },
      });
      return response.data; // Повертаємо дані користувача
    } catch (err) {
      console.error(`Error fetching user by ID (${userId}):`, err);
      throw err; // Кидаємо помилку, щоб обробити її локально
    } finally {
      setLoading(false);
    }
  };

  // Отримати поточного користувача
  const getCurrentUser = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}users/get-current-user`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setCurrentUser(response.data);
    } catch (err) {
      setError(err.message);
      console.error("Error fetching current user:", err);
    } finally {
      setLoading(false);
    }
  };
  
  // Отримати всіх активних користувачів
  const getAllActiveUsers = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}users/get-all-users-were-is-active`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUsers(response.data); // Зберігаємо активних користувачів
    } catch (err) {
      setError(err.message);
      console.error("Error fetching active users:", err);
    } finally {
      setLoading(false);
    }
  }, []);
  
      return (
        <GlobalContext.Provider
          value={{
            users,
            currentUser,
            loading,
            error,
            getAllUsers,
            getUserById,
            getCurrentUser,
            getAllActiveUsers,
          }}
        >
          {children}
        </GlobalContext.Provider>
      );
    };

export const useGlobalContext = () => {
  return useContext(GlobalContext);
};