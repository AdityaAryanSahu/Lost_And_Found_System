import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import apiClient from '../api/apiClient';
import './Profile.css'; // The stylesheet with the dark/gold theme

const ProfilePage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [userItems, setUserItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/auth');
      return;
    }
    
    const fetchUserItems = async () => {
      try {
        const response = await apiClient.get('/items/');
        const myItems = (response.data.item_list || []).filter(
          item => item.user_id === user.user_id
        );
        setUserItems(myItems);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserItems();
  }, [user, navigate]);

  if (!user) return null;

  return (
    <div className="profile-page">
      <div className="profile-container">
        
        {/* Header */}
        <div className="profile-header">
          <button 
            onClick={() => navigate('/items')} 
            className="back-btn"
          >
            ← Back
          </button>
          <h1>My Profile</h1>
          <button 
            onClick={() => { logout(); navigate('/auth'); }} 
            className="logout-btn"
          >
            Logout
          </button>
        </div>

        {/* Profile Info Card */}
        <div className="profile-card">
          <div className="profile-avatar">
            {user.user_id?.charAt(0).toUpperCase()}
          </div>
          <h2 className="user-id">{user.user_id}</h2>
          <p className="user-email">{user.email || 'No email'}</p>
          
          <div className="user-stats">
            <div className="stat">
              <h3>{userItems.length}</h3>
              <p>Posts</p>
            </div>
            <div className="stat">
              <h3>{userItems.filter(item => item.is_claimed).length}</h3>
              <p>Claimed</p>
            </div>
            <div className="stat">
              <h3>{userItems.filter(item => !item.is_claimed).length}</h3>
              <p>Available</p>
            </div>
          </div>
        </div>

        {/* My Uploads Section */}
        <div className="my-uploads-section">
          <h2>My Uploads ({userItems.length})</h2>
          {loading ? (
            <p className="no-items">Loading...</p>
          ) : userItems.length === 0 ? (
            <div className="no-items">
              <p>No items posted yet</p>
              <button 
                onClick={() => navigate('/upload-item')}
              >
                Post Item
              </button>
            </div>
          ) : (
            <div className="items-grid">
              {userItems.map(item => (
                <div 
                  key={item.item_id}
                  onClick={() => navigate(`/items/${item.item_id}`)}
                  style={{ 
                    cursor: 'pointer',
                    border: '1px solid #333', 
                    borderRadius: '8px',
                    overflow: 'hidden',
                    background: '#232323',
                    transition: 'all 0.3s',
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.transform = 'translateY(-4px)';
                    e.currentTarget.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.6)';
                    e.currentTarget.style.borderColor = '#D4AF37';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                    e.currentTarget.style.borderColor = '#333';
                  }}
                >
                  {item.img?.[0]?.url ? (
                    <img src={item.img[0].url} alt={item.desc} style={{ width: '100%', height: '200px', objectFit: 'cover' }} />
                  ) : (
                    <div style={{ 
                        width: '100%', 
                        height: '200px', 
                        background: '#333333', 
                        display: 'flex', 
                        alignItems: 'center', 
                        justifyContent: 'center', 
                        fontSize: '48px',
                        color: '#666'
                    }}>
                      📷
                    </div>
                  )}
                  <div style={{ padding: '16px', color: '#CCCCCC' }}>
                    <h3 style={{ margin: '0 0 8px 0', color: '#D4AF37' }}>{item.type}</h3>
                    <p style={{ fontSize: '14px', color: '#999' }}>{item.desc}</p>
                    <p style={{ 
                        fontSize: '14px', 
                        color: item.is_claimed ? '#e74c3c' : '#27ae60'
                    }}>
                      {item.is_claimed ? '● Claimed' : '● Available'}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;