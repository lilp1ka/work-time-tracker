import axios from 'axios';

const API_BASE_URL = "https://your-api-url.com/users";

export const getAllUsers = async () => {
  const response = await axios.get(`${API_BASE_URL}/get-all-users`);
  return response.data;
};

export const getUserById = async (userId) => {
  const response = await axios.get(`${API_BASE_URL}/get-user-by-id`, {
    params: { user_id: userId },
  });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await axios.get(`${API_BASE_URL}/get-current-user`);
  return response.data;
};

export const getActiveUsers = async () => {
  const response = await axios.get(`${API_BASE_URL}/get-all-users-were-is-active`);
  return response.data;
};
