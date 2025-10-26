// src/api/authService.js
import apiClient from './apiClient';

/**
 * Registers a new user.
 */
export const registerUser = async (userData) => {
  return apiClient.post('/auth/register', userData);
};

/**
 * Logs in a user.
 */
export const loginUser = async (credentials) => {
  // Returns the LoginResponse which contains the JWT token
  return apiClient.post('/auth/login', credentials);
};

/**
 * Fetches the currently authenticated user's profile details.
 */
export const fetchCurrentUser = async () => {
  // Calls GET /users/me
  return apiClient.get('/users/me');
};

/**
 * Updates the user's profile (e.g., email).
 */
export const updateUserProfile = async (updateData) => {
  // Calls PUT /users/me
  return apiClient.put('/users/me', updateData);
};