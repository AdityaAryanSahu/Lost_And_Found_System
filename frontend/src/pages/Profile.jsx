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
    // Applied dark background via external CSS in index.css or global file
    <div style={{ padding: '20px', minHeight: '100vh', background: '#0a0a0a' }}> 
      
      <div className="profile-container"> {/* Container Class Applied */}
        
        {/* Header - Use class and retain inline onClick functions */}
        <div className="profile-header">
          <button 
            onClick={() => navigate('/items')} 
            className="back-btn" // Class Applied
          >
            ← Back
          </button>
          <h1>My Profile</h1>
          <button 
            onClick={() => { logout(); navigate('/auth'); }} 
            className="logout-btn" // Class Applied
          >
            Logout
          </button>
        </div>

        {/* Profile Info - Use Profile Card Class */}
        <div className="profile-card">
          <div className="profile-avatar"> {/* Avatar Class Applied (Gold/Black) */}
            {user.user_id?.charAt(0).toUpperCase()}
          </div>
          <h2 className="user-id">{user.user_id}</h2> {/* User ID Class Applied */}
          <p className="user-email">{user.email || 'No email'}</p> {/* Email Class Applied */}
          
          <div className="user-stats"> {/* Stats Container Class Applied */}
            <div className="stat">
              <h3>{userItems.length}</h3> {/* Stat H3 Class Applied (Gold) */}
              <p>Posts</p> {/* Stat P Class Applied (Light Gray) */}
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
          <h2>My Uploads ({userItems.length})</h2> {/* Uploads H2 Class Applied (Gold) */}
          {loading ? (
            <p className="no-items">Loading...</p>
          ) : userItems.length === 0 ? (
            <div className="no-items"> {/* No Items Class Applied */}
              <p>No items posted yet</p>
              <button 
                onClick={() => navigate('/upload-item')}
                // This button gets its gold style from the .no-items button rule in Profile.css
              >
                Post Item
              </button>
            </div>
          ) : (
            <div className="items-grid"> {/* Items Grid Class Applied */}
              {userItems.map(item => (
                <div 
                  key={item.item_id}
                  onClick={() => navigate(`/items/${item.item_id}`)}
                  style={{ 
                    cursor: 'pointer',
                    // Retaining item card specific styles for background/hover transition
                    border: '1px solid #333', 
                    borderRadius: '8px',
                    overflow: 'hidden',
                    background: '#232323', // Dark background for the card
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
                    <h3 style={{ margin: '0 0 8px 0', color: '#D4AF37' }}>{item.type}</h3> {/* Gold type heading */}
                    <p style={{ fontSize: '14px', color: '#999' }}>{item.desc}</p>
                    <p style={{ 
                        fontSize: '14px', 
                        color: item.is_claimed ? '#e74c3c' : '#27ae60' // Retaining status colors for meaning
                    }}>
                      {item.is_claimed ? '✅ Claimed' : '🔍 Available'}
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