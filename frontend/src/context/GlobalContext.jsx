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



  const inviteUserToTeam = async (teamId, email) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}team_user/add_user_to_team`,
        { team_id: teamId, email },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      return response.data;
    } catch (err) {
      console.error(err.response?.data?.detail || "Не вдалося надіслати запрошення.");
      throw err;
    }
  };

  const createTeam = async (teamName) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}teams/create_team`,
        { name: teamName },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      return response.data;
    } catch (err) {
      console.error(err.response?.data?.detail || "Помилка створення команди");
      throw err;
    }
  };

  const changeTeamName = async (teamId, newName) => {
    try {
      const response = await axios.patch(
        `${API_BASE_URL}teams/change_team_name`,
        { team_id: teamId, new_name: newName },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      return response.data;
    } catch (err) {
      console.error(err.response?.data?.detail || "Помилка зміни назви команди");
      throw err;
    }
  };

  const deleteTeam = async (teamId) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}teams/delete_team`, {
        data: { team_id: teamId },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (err) {
      console.error(err.response?.data?.detail || "Помилка видалення команди");
      throw err;
    }
  };

  const getTeamUsers = async (teamId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}team_user/team_users`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: { team_id: teamId },
      });
      return response.data;
    } catch (err) {
      console.error(err.response?.data?.detail || "Помилка отримання учасників команди");
      throw err;
    }
  };

  const removeUserFromTeam = async (teamId, userId) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}team_user/remove_user_from_team`, {
        data: { team_id: teamId, user_id: userId },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (err) {
      console.error(err.response?.data?.detail || "Помилка видалення користувача з команди");
      throw err;
    }
  };

  const getTeamInfo = async (teamId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}teams/team_info`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: { team_id: teamId },
      });
      return response.data;
    } catch (err) {
      console.error(err.response?.data?.detail || "Помилка отримання інформації про команду");
      throw err;
    }
  };

  const getMyTeams = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}team_user/my_teams`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data.teams;
    } catch (err) {
      console.error(err.response?.data?.detail || "Помилка отримання списку команд");
      throw err;
    }
  };

  


  
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
            inviteUserToTeam,
            createTeam,
            getTeamInfo,
            changeTeamName,
            deleteTeam,
            getTeamUsers,
            removeUserFromTeam,
            getMyTeams,
          }}
        >
          {children}
        </GlobalContext.Provider>
      );
    };

export const useGlobalContext = () => {
  return useContext(GlobalContext);
};