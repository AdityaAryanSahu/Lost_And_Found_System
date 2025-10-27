// src/components/ChatWindow.jsx
import React, { useState, useEffect, useRef } from 'react';
import apiClient from '../api/apiClient';
import { useAuth } from '../contexts/AuthContext';
import './ChatWindow.css';

const ChatWindow = ({ conversationId, conversation }) => {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Fetch messages function (can be called multiple times)
  const fetchMessages = async () => {
    if (!conversationId || !user) return;
    
    try {
      const response = await apiClient.get(`/messages/conversations/${conversationId}`);
      setMessages(response.data.messages || []);
      setError(null);
    } catch (err) {
      console.error("Failed to fetch messages:", err);
      setError("Failed to load messages.");
    } finally {
      setLoading(false);
    }
  };

  // Set up polling for real-time updates
  useEffect(() => {
    if (!conversationId || !user) return;

    setLoading(true);
    fetchMessages(); // Initial fetch

    // Poll every 3 seconds for new messages
    const pollInterval = setInterval(() => {
      fetchMessages();
    }, 3000);

    // Cleanup on unmount or conversation change
    return () => {
      clearInterval(pollInterval);
    };
  }, [conversationId, user]);

  // Auto-scroll when messages update
  useEffect(() => {
    if (messages.length > 0) {
      setTimeout(scrollToBottom, 100);
    }
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !conversationId || !user) return;

    const participants = conversation?.participant_ids || [];
    const receiverId = participants.find(id => id !== user.user_id) || '';

    const payload = {
      receiver_id: receiverId,
      content: newMessage.trim(),
    };

    const tempMessage = {
      message_id: Date.now().toString(),
      sender_id: user.user_id,
      content: newMessage.trim(),
      created_at: new Date().toISOString(),
      status: 'sent',
    };

    setMessages(prev => [...prev, tempMessage]);
    setNewMessage('');

    try {
      const response = await apiClient.post('/messages/send', payload);
      setMessages(prev => prev.map(msg => 
        msg.message_id === tempMessage.message_id ? response.data : msg
      ));
      scrollToBottom();
    } catch (err) {
      console.error("Failed to send message:", err);
      setMessages(prev => prev.filter(msg => msg.message_id !== tempMessage.message_id));
      setError("Failed to send message.");
    }
  };

  if (!user) {
    return <div className="chat-window">Loading user...</div>;
  }

  if (!conversationId) {
    return (
      <div className="chat-window">
        <div className="no-conversation">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          <p>Select a conversation to start messaging</p>
        </div>
      </div>
    );
  }

  const otherParticipant = conversation?.participant_ids?.find(id => id !== user.user_id);
  const participantName = otherParticipant ? `User ${otherParticipant.substring(0, 15)}` : 'User';

  return (
    <div className="chat-window">
      <div className="chat-header">
        <div className="chat-header-info">
          <div className="chat-avatar">
            {participantName.charAt(0).toUpperCase()}
          </div>
          <div className="chat-header-text">
            <h3>{participantName}</h3>
            <span className="online-status"></span>
          </div>
        </div>
        <div className="chat-header-actions">
          <button className="icon-button" title="Search">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
          </button>
          <button className="icon-button" title="More">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="1"/>
              <circle cx="12" cy="5" r="1"/>
              <circle cx="12" cy="19" r="1"/>
            </svg>
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}
      
      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading messages...</p>
        </div>
      ) : (
        <div className="messages-container">
          {messages.map((msg) => (
            <div
              key={msg.message_id}
              className={`message ${msg.sender_id === user.user_id ? 'sent' : 'received'}`}
            >
              <div className="message-content">{msg.content}</div>
              <div className="message-time">
                {new Date(msg.created_at).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      )}

      <form onSubmit={handleSend} className="message-input-form">
        <button type="button" className="icon-button-input">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="1"/>
            <circle cx="12" cy="5" r="1"/>
            <circle cx="19" cy="12" r="1"/>
            <circle cx="5" cy="12" r="1"/>
          </svg>
        </button>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
          className="message-input"
        />
        <button type="submit" disabled={!newMessage.trim()} className="send-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
          </svg>
        </button>
      </form>
    </div>
  );
};

export default ChatWindow;
