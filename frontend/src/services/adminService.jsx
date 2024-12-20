import axios from 'axios';

const API_BASE_URL = "https://your-api-url.com";

export const setUserTasks = async (userId, tasks) => {
  const response = await axios.post(`${API_BASE_URL}/tasks/set-tasks`, {
    user_id: userId,
    tasks,
  });
  return response.data;
};

export const getUserActivity = async () => {
  const response = await axios.get(`${API_BASE_URL}/activity/get-activity`);
  return response.data;
};

