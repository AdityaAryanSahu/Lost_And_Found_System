// src/api/claimService.js
import apiClient from './apiClient';

/**
 * Submits a claim for a lost item.
 */
export const submitClaim = async (claimData) => {
  // Calls POST /claims
  return apiClient.post('/claims', claimData);
};

/**
 * Gets claims for a specific item (for the item poster to review).
 */
export const getClaimsByItem = async (itemId) => {
  // Calls GET /claims/item/{itemId}
  return apiClient.get(`/claims/item/${itemId}`);
};

/**
 * Reviews a claim (Approves or Rejects).
 */
export const reviewClaim = async (claimId, action) => {
  // Calls POST /claims/{claimId}/review/{action}
  return apiClient.post(`/claims/${claimId}/review/${action}`);
};