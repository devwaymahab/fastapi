import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Replace with your FastAPI backend URL
});

export const login = async (email, password) => {
  try {
    const response = await API.post('/login', { email, password });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : error;
  }
};

export default API;