import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import apiClient from '../api/apiClient';
import './MyItems.css';

const MyItemsPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [myItems, setMyItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/auth');
      return;
    }

    const fetchMyItems = async () => {
      try {
        const response = await apiClient.get('/items/');
        const userItems = (response.data.item_list || []).filter(
          item => item.user_id === user.user_id
        );
        setMyItems(userItems);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMyItems();
  }, [user, navigate]);

  if (!user) return null;

  return (
    <div className="my-items-page">
      <div className="my-items-container">
        
        {/* Header */}
        <div className="my-items-header">
          <button 
            onClick={() => navigate('/items')} 
            className="back-btn"
          >
            ← Back
          </button>
          <h1>My Uploads</h1>
        </div>

        {/* Content */}
        <div style={{ 
          maxWidth: '1200px', 
          margin: '0 auto', 
          background: '#1f1f1f',
          padding: '30px', 
          borderRadius: '12px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.4)',
          position: 'relative',
          zIndex: 10
        }}>
          {loading ? (
            <p style={{ color: '#CCCCCC' }}>Loading your items...</p>
          ) : myItems.length === 0 ? (
            <div className="no-items-message">
              <p>You haven't posted any items yet</p>
              <button 
                onClick={() => navigate('/upload-item')}
                className="upload-btn"
              >
                Post Your First Item
              </button>
            </div>
          ) : (
            <>
              <p style={{ marginBottom: '20px', color: '#B8B8B8' }}>Total Items: {myItems.length}</p>
              <div className="my-items-grid">
                {myItems.map(item => (
                  <div 
                    key={item.item_id}
                    className="item-card"
                    onClick={() => navigate(`/items/${item.item_id}`)}
                  >
                    <div className="item-image-container">
                      {item.img?.[0]?.url ? (
                        <img src={item.img[0].url} alt={item.desc} className="item-image" />
                      ) : (
                        <div className="no-image">📷</div>
                      )}
                      
                      <div 
                        className="item-type-badge"
                        style={{
                          background: 'linear-gradient(135deg, #b8941f 0%, #d4af37 100%)',
                        }}
                      >
                        {item.type}
                      </div>

                      {item.is_claimed && (
                        <div className="claimed-badge">
                          ✓ Claimed
                        </div>
                      )}
                    </div>

                    <div className="item-details">
                      <h3>{item.type}</h3>
                      <div className="item-meta">
                        <p>
                          <span className="meta-icon">📍</span>
                          {item.desc}
                        </p>
                        <p>
                          <span className="meta-icon">📅</span>
                          {new Date(item.created_at).toLocaleDateString()}
                        </p>
                        <p className={item.is_claimed ? 'status-claimed' : 'status-available'}>
                          {item.is_claimed ? '● Claimed' : '● Available'}
                        </p>
                      </div>
                      <button className="view-details-btn">
                        View Details
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default MyItemsPage;