import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import apiClient from '../api/apiClient';
// 1. IMPORT YOUR SERVICES
import { getClaimsByItem, reviewClaim } from '../api/claimService';
import './MyItems.css';

const MyItemsPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [myItems, setMyItems] = useState([]);
  const [loading, setLoading] = useState(true);

  // 2. NEW STATES FOR THE CLAIMS MODAL
  const [selectedItem, setSelectedItem] = useState(null);
  const [claims, setClaims] = useState([]);
  const [loadingClaims, setLoadingClaims] = useState(false);

  useEffect(() => {
    if (!user) {
      navigate('/auth');
      return;
    }

    fetchMyItems();
  }, [user, navigate]);

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

  // 3. OPEN MODAL & FETCH CLAIMS
  const handleOpenClaims = async (e, item) => {
    e.stopPropagation(); // Prevents the card click from navigating to the detail page
    setSelectedItem(item);
    setLoadingClaims(true);
    setClaims([]); // Clear old claims

    try {
      const response = await getClaimsByItem(item.item_id);
      setClaims(response.data || []);
    } catch (err) {
      console.error('Error fetching claims:', err);
    } finally {
      setLoadingClaims(false);
    }
  };

  // 4. HANDLE APPROVE/REJECT
  const handleReviewClaim = async (claimId, action) => {
    if (!window.confirm(`Are you sure you want to ${action} this claim?`)) {
      return;
    }

    try {
      await reviewClaim(claimId, action);
      alert(`Claim ${action.toLowerCase()}d successfully!`);
      
      // Update the local state so the UI reflects the change instantly
      if (action === 'APPROVE') {
        // Mark the item as claimed in the background dashboard
        setMyItems(prev => prev.map(i => 
          i.item_id === selectedItem.item_id ? { ...i, is_claimed: true } : i
        ));
        // Update the selected item
        setSelectedItem(prev => ({ ...prev, is_claimed: true }));
      }

      // Refetch claims to update their status badges in the modal
      const response = await getClaimsByItem(selectedItem.item_id);
      setClaims(response.data || []);
      
    } catch (err) {
      console.error(`Error trying to ${action} claim:`, err);
      const errorMsg = err.response?.data?.detail || `Failed to ${action} claim`;
      alert(`Error: ${errorMsg}`);
    }
  };

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
                        style={{ background: 'linear-gradient(135deg, #b8941f 0%, #d4af37 100%)' }}
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
                        <p><span className="meta-icon">📍</span>{item.desc}</p>
                        <p><span className="meta-icon">📅</span>{new Date(item.created_at).toLocaleDateString()}</p>
                        <p className={item.is_claimed ? 'status-claimed' : 'status-available'}>
                          {item.is_claimed ? '● Claimed' : '● Available'}
                        </p>
                      </div>
                      
                      {/* 🚨 UPDATED BUTTONS */}
                      <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
                        <button className="view-details-btn" style={{ flex: 1 }}>
                          View Details
                        </button>
                        <button 
                          className="view-claims-btn" 
                          style={{ flex: 1, background: '#d4af37', color: '#000', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}
                          onClick={(e) => handleOpenClaims(e, item)}
                        >
                          Review Claims
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>

      {/* 5. THE CLAIMS MODAL */}
      {selectedItem && (
        <div className="modal-overlay" onClick={() => setSelectedItem(null)}>
          <div className="modal-content claims-modal" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '600px', width: '90%', maxHeight: '80vh', overflowY: 'auto', background: '#2a2a2a', color: '#fff', padding: '30px', borderRadius: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #444', paddingBottom: '15px', marginBottom: '20px' }}>
              <h2>Claims for: {selectedItem.type}</h2>
              <button onClick={() => setSelectedItem(null)} style={{ background: 'transparent', color: '#fff', border: 'none', fontSize: '20px', cursor: 'pointer' }}>✖</button>
            </div>

            {loadingClaims ? (
              <p>Loading claims...</p>
            ) : claims.length === 0 ? (
              <p style={{ color: '#aaa', textAlign: 'center', padding: '20px 0' }}>No claims have been submitted for this item yet.</p>
            ) : (
              <div className="claims-list" style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                {claims.map((claim) => (
                  <div key={claim.claim_id} style={{ padding: '15px', border: '1px solid #444', borderRadius: '8px', background: '#333' }}>
                    <p><strong>Claimant ID:</strong> User {claim.user_id}</p>
                    <p><strong>Submitted:</strong> {new Date(claim.submitted_at).toLocaleDateString()}</p>
                    <p style={{ margin: '10px 0', padding: '10px', background: '#222', borderRadius: '4px' }}>
                      <em>"{claim.justification}"</em>
                    </p>
                    <p>
                      <strong>Status: </strong> 
                      <span style={{ 
                        color: claim.status === 'APPROVE' ? '#4CAF50' : claim.status === 'REJECT' ? '#F44336' : '#FF9800',
                        fontWeight: 'bold' 
                      }}>
                        {claim.status}
                      </span>
                    </p>
                    
                    {claim.status === 'PENDING' && !selectedItem.is_claimed && (
                      <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
                        <button 
                          onClick={() => handleReviewClaim(claim.claim_id, 'APPROVE')} 
                          style={{ flex: 1, background: '#4CAF50', color: 'white', padding: '10px', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold' }}
                        >
                          Approve
                        </button>
                        <button 
                          onClick={() => handleReviewClaim(claim.claim_id, 'REJECT')}
                          style={{ flex: 1, background: '#F44336', color: 'white', padding: '10px', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold' }}
                        >
                          Reject
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default MyItemsPage;