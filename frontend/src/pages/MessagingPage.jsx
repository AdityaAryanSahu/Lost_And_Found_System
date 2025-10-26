// src/pages/MessagingPage.jsx
import React, { useState } from 'react';
import ConversationList from '../components/ConversationList';
import ChatWindow from '../components/ChatWindow';
import './MessagingPage.css';

const MessagingPage = () => {
  const [selectedConversationId, setSelectedConversationId] = useState(null);
  const [selectedConversation, setSelectedConversation] = useState(null);

  const handleSelectConversation = (conversationId, conversation) => {
    setSelectedConversationId(conversationId);
    setSelectedConversation(conversation);
  };

  return (
    <div className="messaging-page">
      <ConversationList 
        onSelectConversation={handleSelectConversation}
        selectedConversationId={selectedConversationId}
      />
      <ChatWindow 
        conversationId={selectedConversationId}
        conversation={selectedConversation}
      />
    </div>
  );
};

export default MessagingPage;
