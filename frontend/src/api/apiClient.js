import axios from 'axios';

const API_URL =  process.env.REACT_APP_API_URL || 'http://localhost:8000';


const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to every request 
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    console.log('📤 Sending request with token:', token ? 'Yes' : 'No');
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle 401 - logout user
apiClient.interceptors.response.use(
  res => res,
  async err => {
    if (err.response?.status === 401) {
      const refresh = localStorage.getItem("refresh_token");
      const res = await apiClient.post("/auth/refresh", { refresh_token: refresh });
      localStorage.setItem("access_token", res.data.access_token);
      err.config.headers.Authorization = `Bearer ${res.data.access_token}`;
      return apiClient(err.config);
    }
    return Promise.reject(err);
  }
);

export default apiClient;