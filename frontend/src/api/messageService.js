// src/api/messageService.js
import apiClient from './apiClient';

/**
 * Fetches the list of conversations for the current user.
 */
export const getConversations = async () => {
  // Calls GET /messages/conversations
  return apiClient.get('/messages/conversations');
};

/**
 * Fetches the message history for a specific conversation.
 */
export const getConversationMessages = async (conversationId, params = {}) => {
  // Calls GET /messages/conversations/{conversationId}
  return apiClient.get(`/messages/conversations/${conversationId}`, { params });
};

/**
 * Sends a new message (used both for starting new chats and replying).
 */
export const sendMessage = async (messageData) => {
  // Calls POST /messages/send
  return apiClient.post('/messages/send', messageData);
};