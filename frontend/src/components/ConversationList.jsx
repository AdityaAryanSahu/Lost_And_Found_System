// src/components/ConversationList.jsx
import React, { useEffect, useState } from 'react';
import { getConversations } from '../api/messageService';
import { useAuth } from '../contexts/AuthContext';
import './ConversationList.css';

const ConversationList = ({ onSelectConversation, selectedConversationId }) => {
  const { user } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

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

  const getParticipantName = (conv) => {
    if (!user || !conv.participant_ids) return 'Unknown';
    const otherId = conv.participant_ids.find(id => id !== user.user_id);
    return otherId ? `User ${otherId.substring(0, 8)}` : 'Unknown';
  };

  const getInitial = (name) => {
    // For generated names like "User 23090556", just use the first letter + first digit
    const parts = name.trim().split(' ');
    if (parts.length >= 2) {
      const second = parts[1];
      // If second part is a number/ID, just use first letter of first part
      if (/^\d/.test(second)) return parts[0][0].toUpperCase();
      return (parts[0][0] + second[0]).toUpperCase();
    }
    return name.charAt(0).toUpperCase() || 'U';
  };

  const filteredConversations = conversations.filter((conv) => {
    if (!searchQuery.trim()) return true;
    const name = getParticipantName(conv).toLowerCase();
    const preview = (conv.last_message_content || '').toLowerCase();
    return name.includes(searchQuery.toLowerCase()) || preview.includes(searchQuery.toLowerCase());
  });

  if (loading) {
    return (
      <div className="conversation-list">
        <div className="conversation-list-header">
          <h2>Messages</h2>
        </div>
        <div className="loading-state">
          <div className="spinner" />
          <p>Loading conversations…</p>
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

  const totalUnread = conversations.reduce((sum, c) => sum + (c.unread_count || 0), 0);

  return (
    <div className="conversation-list">
      {/* Header */}
      <div className="conversation-list-header">
        <h2>Messages</h2>
        <span className="conversation-count">
          {totalUnread > 0 ? `${totalUnread} new` : conversations.length}
        </span>
      </div>

      {/* Search */}
      <div className="search-container">
        <div className="search-wrapper">
          <span className="search-icon">⌕</span>
          <input
            type="text"
            className="search-input"
            placeholder="Search conversations…"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Conversation items */}
      {filteredConversations.length === 0 ? (
        <div className="empty-state">
          <svg width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
          {searchQuery ? (
            <>
              <p>No results for "{searchQuery}"</p>
              <span>Try a different name or message</span>
            </>
          ) : (
            <>
              <p>No messages yet</p>
              <span>Start a conversation by contacting a seller</span>
            </>
          )}
        </div>
      ) : (
        <>
        <div className="conversation-items">
          {filteredConversations.map((conv) => {
            const participantName = getParticipantName(conv);
            const initials = getInitial(participantName);
            const isActive = selectedConversationId === conv.conversation_id;
            const isOnline = conv.is_online || false;

            return (
              <div
                key={conv.conversation_id}
                className={`conversation-item ${isActive ? 'active' : ''}`}
                onClick={() => onSelectConversation(conv.conversation_id, conv)}
              >
                <div className="conversation-avatar">
                  <div className="avatar-circle">{initials}</div>
                  {isOnline && <div className="online-indicator" />}
                </div>

                <div className="conversation-content">
                  <div className="conversation-header">
                    <h4 className="conversation-name">{participantName}</h4>
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
        <div className="conversation-list-spacer" />
        </>
      )}
    </div>
  );
};

export default ConversationList;