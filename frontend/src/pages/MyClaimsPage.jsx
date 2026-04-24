import React, { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';
import './MyClaimsPage.css'; 

const MyClaimsPage = () => {
  const [myClaims, setMyClaims] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMyClaims();
  }, []);

  const fetchMyClaims = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/claims/my-claims');
      setMyClaims(response.data);
    } catch (err) {
      console.error("Error fetching claims", err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusClass = (status) => {
    if (status === 'APPROVE') return 'status-approve';
    if (status === 'REJECT') return 'status-reject';
    return 'status-pending';
  };

  return (
    <div className="my-claims-page">
      <h1 className="my-claims-header">Claims Submitted</h1>
      
      {loading ? (
        <div style={{ textAlign: 'center', color: '#d4af37' }}>Loading claims...</div>
      ) : (
        <div className="claims-list">
          {myClaims.map(claim => (
            <div key={claim.claim_id} className="claim-card">
              
              <div className="claim-card-header">
                <h3>Item ID: {claim.item_id}</h3>
                <span className={`status-badge ${getStatusClass(claim.status)}`}>
                  {claim.status}
                </span>
              </div>

              <p className="claim-justification">"{claim.justification}"</p>

              {/* 🚨 THE SECURE PIN DISPLAY FOR THE OWNER 🚨 */}
              {claim.status === 'APPROVE' && !claim.is_returned && (
                <div className="secure-pin-box">
                  <p>Your claim was approved! Give this PIN to the finder when you meet to receive your item:</p>
                  <h1 className="pin-display">
                    {claim.handoff_pin}
                  </h1>
                </div>
              )}

              {/* IF RETURNED */}
              {claim.is_returned && (
                <div className="returned-banner">
                   Item successfully recovered!
                </div>
              )}

            </div>
          ))}
          
          {!loading && myClaims.length === 0 && (
            <p className="no-claims-text">You haven't submitted any claims yet.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default MyClaimsPage;