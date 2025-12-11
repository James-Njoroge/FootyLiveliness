import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'https://footyliveliness.onrender.com';

export const fetchUpcomingMatches = async () => {
  const response = await axios.get(`${API_URL}/api/upcoming`);
  return response.data;
};

export const predictMatch = async (homeTeam, awayTeam) => {
  const response = await axios.post(`${API_URL}/api/predict`, {
    home: homeTeam,
    away: awayTeam
  });
  return response.data;
};

export const getModelStats = async () => {
  const response = await axios.get(`${API_URL}/api/stats`);
  return response.data;
};

export const checkHealth = async () => {
  const response = await axios.get(`${API_URL}/api/health`);
  return response.data;
};
