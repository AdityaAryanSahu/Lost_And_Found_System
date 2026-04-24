import apiClient from './apiClient';

/**
 * Sends a search request to the matching engine
 * @param {Object} searchRequest - { search_type: string, keywords: string[], location: string }
 */
export const findMatches = async (searchRequest) => {
  // Assuming your match_router is mounted at /matches in your FastAPI main.py
  return apiClient.post('/matches/', searchRequest);
};