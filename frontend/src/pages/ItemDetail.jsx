import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import apiClient from '../api/apiClient';
import './ItemDetail.css';

const ItemDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sendingMessage, setSendingMessage] = useState(false);
  
  // Claim modal state
  const [showClaimModal, setShowClaimModal] = useState(false);
  const [claimDetails, setClaimDetails] = useState('');
  const [submittingClaim, setSubmittingClaim] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    if (!user) {
      navigate('/auth');
      return;
    }
    fetchItemDetails();
  }, [id, user, navigate]);

  const fetchItemDetails = async () => {
    try {
      const response = await apiClient.get(`/items/${id}`);
      setItem(response.data);
    } catch (err) {
      console.error('Error fetching item:', err);
      setError('Failed to load item details');
    } finally {
      setLoading(false);
    }
  };

  const handleContactSeller = async () => {
    // Add null checks
    if (!user) {
      alert("Please log in to contact the seller");
      navigate('/auth');
      return;
    }

    if (!item) {
      alert("Item data not loaded");
      return;
    }

    if (item.user_id === user.user_id) {
      alert("You can't message yourself! This is your own post.");
      return;
    }

    setSendingMessage(true);

    try {
      const payload = {
        receiver_id: item.user_id,
        content: `Hi! I'm interested in your ${item.type}: "${item.desc}". Is it still available?`,
        item_id: item.item_id
      };

      console.log('Sending message:', payload); // Debug log

      await apiClient.post('/messages/send', payload);
      navigate('/messages');
    } catch (err) {
      console.error('Error starting conversation:', err);
      const errorMsg = err.response?.data?.detail || 'Failed to start conversation';
      alert(`Error: ${errorMsg}`);
    } finally {
      setSendingMessage(false);
    }
  };

  const handleClaimSubmit = async (e) => {
    e.preventDefault();
    
    if (!user) {
      alert("Please log in to claim items");
      navigate('/auth');
      return;
    }

    if (!claimDetails.trim()) {
      alert('Please provide claim details');
      return;
    }

    if (!item) {
      alert("Item data not loaded");
      return;
    }

    setSubmittingClaim(true);

    try {
      const payload = {
        receiver_id: item.user_id,
        content: `I'd like to claim this ${item.type} "${item.desc}". Details: ${claimDetails}`,
        item_id: item.item_id
      };

      await apiClient.post('/messages/send', payload);
      
      alert('Claim request sent successfully!');
      setShowClaimModal(false);
      setClaimDetails('');
      navigate('/messages');
    } catch (err) {
      console.error('Error submitting claim:', err);
      alert('Failed to submit claim. Please try again.');
    } finally {
      setSubmittingClaim(false);
    }
  };

  // NEW: Mark as Claimed Handler
  const handleMarkAsClaimed = async () => {
    if (!window.confirm('Mark this item as claimed? This will hide it from search results.')) {
      return;
    }

    try {
      await apiClient.patch(`/items/${item.item_id}/claim`, {
        is_claimed: true
      });
      
      alert('Item marked as claimed successfully!');
      fetchItemDetails(); // Refresh the item data
    } catch (err) {
      console.error('Error marking item as claimed:', err);
      const errorMsg = err.response?.data?.detail || 'Failed to mark item as claimed';
      alert(`Error: ${errorMsg}`);
    }
  };

  // Early returns with null checks
  if (!user) {
    return (
      <div className="item-detail-page">
        <div className="loading">Checking authentication...</div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="item-detail-page">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="item-detail-page">
        <div className="error">{error}</div>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="item-detail-page">
        <div className="error">Item not found</div>
      </div>
    );
  }

  const isOwnItem = item.user_id === user.user_id;

  return (
    <div className="item-detail-page">
      {/* Header */}
      <header className="detail-header">
        <button onClick={() => navigate('/items')} className="back-btn">
          ← Back
        </button>
        <h1>Item Details</h1>
      </header>

      {/* Content */}
      <div className="detail-container">
        {/* Image Section */}
        <div className="detail-image-section">
          {item.img && item.img.length > 0 ? (
            <img src={item.img[0].url} alt={item.desc} className="detail-image" />
          ) : (
            <div className="no-image-large"> No Image</div>
          )}
        </div>

        {/* Info Section */}
        <div className="detail-info-section">
          <div className="item-type-badge-large">{item.type}</div>
          <h2>{item.desc}</h2>
          
          <div className="detail-meta">
            <p><strong>Posted by:</strong> User {item.user_id}</p>
            <p><strong>Date Posted:</strong> {new Date(item.created_at).toLocaleDateString()}</p>
            <p>
              <strong>Status:</strong>
              <span className={item.is_claimed ? 'status-claimed-text' : 'status-available-text'}>
                {item.is_claimed ? ' Claimed' : ' Available'}
              </span>
            </p>
          </div>

          {/* Action Buttons */}
          {!isOwnItem ? (
            <div className="action-buttons">
              {!item.is_claimed && (
                <>
                  <button 
                    onClick={handleContactSeller}
                    className="contact-btn"
                    disabled={sendingMessage}
                  >
                    {sendingMessage ? ' Starting...' : ' Contact Seller'}
                  </button>
                  <button 
                    onClick={() => setShowClaimModal(true)}
                    className="claim-btn"
                  >
                     Claim This Item
                  </button>
                </>
              )}
              {item.is_claimed && (
                <div className="claimed-banner">
                   This item has been claimed
                </div>
              )}
            </div>
          ) : (
            //  OWNER SECTION WITH MARK AS CLAIMED
            <div className="own-item-notice">
              <p> This is your post</p>
              <div className="owner-action-buttons">
                <button 
                  className="edit-btn" 
                  onClick={() => navigate(`/upload-item?edit=${item.item_id}`)}
                >
                   Edit Item
                </button>
                
                {/*  MARK AS CLAIMED BUTTON */}
                {!item.is_claimed && (
                  <button 
                    className="mark-claimed-btn"
                    onClick={handleMarkAsClaimed}
                  >
                     Mark as Claimed
                  </button>
                )}
                
                {item.is_claimed && (
                  <span className="already-claimed-badge">
                     Already Claimed
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Claim Modal */}
      {showClaimModal && (
        <div className="modal-overlay" onClick={() => setShowClaimModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Claim This Item</h2>
            <p>Provide details about how you lost or found this item to claim it:</p>
            
            <form onSubmit={handleClaimSubmit}>
              <textarea
                value={claimDetails}
                onChange={(e) => setClaimDetails(e.target.value)}
                placeholder="Example: I lost this red book near the library on 10/20. It has my name written inside the cover..."
                className="claim-textarea"
                rows="5"
                required
              />
              
              <div className="modal-actions">
                <button 
                  type="button" 
                  onClick={() => setShowClaimModal(false)}
                  className="cancel-btn"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="submit-claim-btn"
                  disabled={submittingClaim}
                >
                  {submittingClaim ? 'Submitting...' : 'Submit Claim'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ItemDetailPage;
