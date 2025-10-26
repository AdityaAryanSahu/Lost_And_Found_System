import React, { useState, useEffect } from 'react';

import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

// --- Color Variables for reference ---
// --color-background-dark: #0a0a0a
// --color-card-dark: #1f1f1f
// --color-accent-gold: #D4AF37
// --color-text-light: #CCCCCC

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
    <div style={{ 
        padding: '20px', 
        background: '#0a0a0a', // Dark page background
        minHeight: '100vh', 
        color: '#CCCCCC' 
    }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '30px' }}>
        <button 
            onClick={() => navigate('/items')} 
            style={{ 
                padding: '10px 20px', 
                background: 'transparent', 
                border: '1px solid #D4AF37', // Gold border
                color: '#D4AF37', // Gold text
                borderRadius: '8px', 
                cursor: 'pointer',
                transition: 'all 0.3s'
            }}
            onMouseOver={(e) => { e.currentTarget.style.backgroundColor = '#D4AF37'; e.currentTarget.style.color = 'black'; }}
            onMouseOut={(e) => { e.currentTarget.style.backgroundColor = 'transparent'; e.currentTarget.style.color = '#D4AF37'; }}
        >
          ← Back
        </button>
        <h1 style={{ margin: 0, color: '#D4AF37' }}>Settings</h1> {/* Gold heading */}
      </div>

      {/* Content */}
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        {/* Account Settings */}
        <div style={{ 
            background: '#1f1f1f', // Dark card background
            padding: '30px', 
            borderRadius: '12px', 
            marginBottom: '20px',
            color: '#CCCCCC' 
        }}>
          <h2 style={{ marginTop: 0, color: '#D4AF37' }}>Account Information</h2> {/* Gold heading */}
          <div style={{ marginBottom: '20px' }}>
            <p><strong>User ID:</strong> {user.user_id}</p>
            <p><strong>Email:</strong> {user.email || 'Not set'}</p>
          </div>
        </div>

        {/* Notification Settings */}
        <div style={{ 
            background: '#1f1f1f', // Dark card background
            padding: '30px', 
            borderRadius: '12px', 
            marginBottom: '20px',
            color: '#CCCCCC' 
        }}>
          <h2 style={{ marginTop: 0, color: '#D4AF37' }}>Notifications</h2> {/* Gold heading */}
          
          <label style={{ display: 'flex', alignItems: 'center', marginBottom: '15px', cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
              style={{ 
                  marginRight: '10px', 
                  width: '20px', 
                  height: '20px', 
                  cursor: 'pointer',
                  // Gold border/focus on checkbox, assuming default browser style is compatible
                  accentColor: '#D4AF37' 
              }}
            />
            <span>Enable push notifications</span>
          </label>

          <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              checked={emailAlerts}
              onChange={(e) => setEmailAlerts(e.target.checked)}
              style={{ 
                  marginRight: '10px', 
                  width: '20px', 
                  height: '20px', 
                  cursor: 'pointer',
                  accentColor: '#D4AF37' 
              }}
            />
            <span>Email alerts for new matches</span>
          </label>
        </div>

        {/* Danger Zone */}
        <div style={{ 
            background: '#1f1f1f', // Dark card background
            padding: '30px', 
            borderRadius: '12px', 
            // Red border remains for danger zone
            border: '2px solid #e74c3c' 
        }}>
          <h2 style={{ marginTop: 0, color: '#e74c3c' }}>Danger Zone</h2> {/* Red heading remains */}
          <p style={{ color: '#B8B8B8', marginBottom: '20px' }}>Once you delete your account, there is no going back.</p> {/* Lighter text */}
          <button 
            style={{ 
              padding: '10px 20px',
              background: '#e74c3c', // Red button remains for deletion
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: '600'
            }}
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