import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Settings.css'; 

const SettingsPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState(true);
  const [emailAlerts, setEmailAlerts] = useState(false);

  useEffect(() => {
    if (!user) {
      navigate('/auth');
    }
  }, [user, navigate]);

  if (!user) return null;

  return (
    <div className="settings-page">
      {/* Header */}
      <div className="settings-header">
        <button 
          onClick={() => navigate('/items')} 
          className="back-btn"
        >
          ← Back
        </button>
        <h1>Settings</h1>
      </div>

      {/* Content */}
      <div className="settings-container">
        {/* Account Settings */}
        <div className="settings-card">
          <h2>Account Information</h2>
          <div className="card-content">
            <p><strong>User ID:</strong> {user.user_id}</p>
            <p><strong>Email:</strong> {user.email || 'Not set'}</p>
          </div>
        </div>

        {/* Notification Settings */}
        <div className="settings-card">
          <h2>Notifications</h2>
          
          <label className="checkbox-label">
            <input 
              type="checkbox" 
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
              className="checkbox-input"
            />
            <span>Enable push notifications</span>
          </label>

          <label className="checkbox-label">
            <input 
              type="checkbox" 
              checked={emailAlerts}
              onChange={(e) => setEmailAlerts(e.target.checked)}
              className="checkbox-input"
            />
            <span>Email alerts for new matches</span>
          </label>
        </div>

        {/* Danger Zone */}
        <div className="settings-card danger-zone">
          <h2>Danger Zone</h2>
          <p>Once you delete your account, there is no going back.</p>
          <button 
            className="delete-btn"
            onClick={() => {
              if (window.confirm('Are you sure you want to delete your account?')) {
                logout();
                navigate('/auth');
              }
            }}
          >
            Delete Account
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;