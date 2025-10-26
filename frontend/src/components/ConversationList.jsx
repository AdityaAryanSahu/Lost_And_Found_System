// src/components/ConversationList.jsx
import React, { useEffect, useState } from 'react';
import { getConversations } from '../api/messageService';
import { useAuth } from '../contexts/AuthContext'; // ✅ Add this
import './ConversationList.css';

const ConversationList = ({ onSelectConversation, selectedConversationId }) => {
  const { user } = useAuth(); // ✅ Add this
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchConversations = async () => {
      setLoading(true);
      try {
        const response = await getConversations();
        setConversations(response.data.conversations || []);
      } catch (err) {
        console.error('Failed to fetch conversations:', err);
        setError('Failed to load conversations');
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
  };

  // ✅ ADD THIS HELPER FUNCTION
  const getOtherParticipant = (participantIds) => {
    if (!user || !participantIds) return 'Unknown';
    const otherId = participantIds.find(id => id !== user.user_id);
    return otherId ? `User ${otherId.substring(0, 8)}` : 'Unknown';
  };

  if (loading) {
    return (
      <div className="conversation-list">
        <div className="conversation-list-header">
          <h2>Messages</h2>
        </div>
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading conversations...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="conversation-list">
        <div className="conversation-list-header">
          <h2>Messages</h2>
        </div>
        <div className="error-state">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="conversation-list">
      <div className="conversation-list-header">
        <h2>Messages</h2>
        <span className="conversation-count">{conversations.length}</span>
      </div>

      {conversations.length === 0 ? (
        <div className="empty-state">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          <p>No messages yet</p>
          <span>Start a conversation by contacting a seller</span>
        </div>
      ) : (
        <div className="conversation-items">
          {conversations.map((conv) => {
            // ✅ Get the other participant's ID (not your own)
            const otherParticipantId = conv.participant_ids?.find(id => id !== user?.user_id);
            const participantName = otherParticipantId 
              ? `User ${otherParticipantId.substring(0, 8)}` 
              : 'Unknown';
            
            return (
              <div
                key={conv.conversation_id}
                className={`conversation-item ${selectedConversationId === conv.conversation_id ? 'active' : ''}`}
                onClick={() => onSelectConversation(conv.conversation_id, conv)}
              >
                <div className="conversation-avatar">
                  <div className="avatar-circle">
                    {participantName.charAt(5)?.toUpperCase() || 'U'}
                  </div>
                  {conv.unread_count > 0 && <div className="online-indicator"></div>}
                </div>

                <div className="conversation-content">
                  <div className="conversation-header">
                    <h4 className="conversation-name">
                      {participantName}
                    </h4>
                    <span className="conversation-time">
                      {formatDate(conv.last_message_at || conv.created_at)}
                    </span>
                  </div>
                  <div className="conversation-preview">
                    <p className={conv.unread_count > 0 ? 'unread' : ''}>
                      {conv.last_message_content || 'No messages yet'}
                    </p>
                    {conv.unread_count > 0 && (
                      <span className="unread-badge">{conv.unread_count}</span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ConversationList;
