import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import apiClient from '../api/apiClient';

// --- Color Variables for reference ---
// --color-background-dark: #0a0a0a
// --color-card-dark: #1f1f1f
// --color-accent-gold: #D4AF37
// --color-text-light: #CCCCCC

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
    <div style={{ 
        padding: '20px', 
        background: '#0a0a0a', // Dark page background
        minHeight: '100vh', 
        color: '#CCCCCC' // Base text color
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
        <h1 style={{ margin: 0, color: '#D4AF37' }}>My Uploads</h1> {/* Gold heading */}
      </div>

      {/* Content */}
      <div style={{ 
        maxWidth: '1200px', 
        margin: '0 auto', 
        background: '#1f1f1f', // Dark content card background
        padding: '30px', 
        borderRadius: '12px',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.4)'
      }}>
        {loading ? (
          <p>Loading your items...</p>
        ) : myItems.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '60px 20px' }}>
            <p style={{ fontSize: '18px', color: '#B8B8B8' }}>You haven't posted any items yet</p> {/* Lighter text */}
            <button 
              onClick={() => navigate('/upload-item')}
              style={{ 
                marginTop: '20px',
                padding: '12px 32px',
                // Gold Gradient
                background: 'linear-gradient(135deg, #b8941f 0%, #d4af37 100%)',
                color: 'black',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer',
                boxShadow: '0 4px 12px rgba(212, 175, 55, 0.4)',
                transition: 'transform 0.2s'
              }}
            >
               Post Your First Item
            </button>
          </div>
        ) : (
          <>
            <p style={{ marginBottom: '20px', color: '#B8B8B8' }}>Total Items: {myItems.length}</p> {/* Lighter text */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '20px' }}>
              {myItems.map(item => (
                <div 
                  key={item.item_id}
                  onClick={() => navigate(`/items/${item.item_id}`)}
                  style={{ 
                    cursor: 'pointer',
                    background: '#232323', // Dark item card background
                    border: '1px solid #333',
                    borderRadius: '8px',
                    overflow: 'hidden',
                    transition: 'transform 0.2s, box-shadow 0.2s'
                  }}
                  onMouseOver={(e) => {
                      e.currentTarget.style.transform = 'translateY(-4px)'; 
                      e.currentTarget.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.6)';
                      e.currentTarget.style.borderColor = '#D4AF37'; // Gold border on hover
                  }}
                  onMouseOut={(e) => {
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.boxShadow = 'none';
                      e.currentTarget.style.borderColor = '#333';
                  }}
                >
                  <div style={{ position: 'relative' }}>
                    <div style={{ 
                      position: 'absolute',
                      top: '12px',
                      right: '12px',
                      // Gold Badge Gradient
                      background: 'linear-gradient(135deg, #b8941f 0%, #d4af37 100%)',
                      color: 'black', // Black text on gold
                      padding: '6px 12px',
                      borderRadius: '20px',
                      fontSize: '12px',
                      fontWeight: '600',
                      textTransform: 'uppercase',
                      zIndex: 10
                    }}>
                      {item.type}
                    </div>
                    {item.img?.[0]?.url ? (
                      <img src={item.img[0].url} alt={item.desc} style={{ width: '100%', height: '200px', objectFit: 'cover' }} />
                    ) : (
                      <div style={{ 
                          width: '100%', 
                          height: '200px', 
                          background: '#333333', // Dark placeholder background
                          color: '#666', // Gray placeholder icon
                          display: 'flex', 
                          alignItems: 'center', 
                          justifyContent: 'center', 
                          fontSize: '48px' 
                      }}>
                        📷
                      </div>
                    )}
                  </div>
                  <div style={{ padding: '16px', textAlign: 'center' }}>
                    <h3 style={{ margin: '0 0 8px 0', fontSize: '18px', color: '#CCCCCC' }}>{item.type}</h3> {/* Light title text */}
                    <p style={{ fontSize: '14px', color: '#999', margin: '4px 0' }}>📍 {item.desc}</p>
                    <p style={{ fontSize: '14px', color: '#999', margin: '4px 0' }}>📅 {new Date(item.created_at).toLocaleDateString()}</p>
                    <p style={{ fontSize: '14px', fontWeight: '600', margin: '4px 0', color: item.is_claimed ? '#e74c3c' : '#27ae60' }}>
                      {item.is_claimed ? ' Claimed' : ' Available'}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default MyItemsPage;