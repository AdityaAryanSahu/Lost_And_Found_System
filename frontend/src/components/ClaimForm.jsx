// src/components/ClaimForm.jsx
import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import apiClient from '../api/apiClient';
import './ClaimForm.css'; // Assume CSS for form styling

const ClaimForm = ({ item_id, item_poster_id, onSuccess, onError }) => {
    const { user } = useAuth();
    const [justification, setJustification] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        onError(null);

        if (!user) {
            onError("You must be logged in to submit a claim.");
            setLoading(false);
            return;
        }

        try {
            const payload = {
                item_id: item_id,
                user_id: user.user_id, // The ID of the claimant (current user)
                justification: justification,
            };

            await apiClient.post('/claims', payload);
            
            setLoading(false);
            onSuccess(); // Notify parent component (ItemDetailPage)
            
        } catch (error) {
            console.error("Claim submission failed:", error.response?.data);
            const detail = error.response?.data?.detail || "Failed to submit claim. Item may be gone.";
            onError(detail);
            setLoading(false);
        }
    };

    return (
        <div className="claim-form-wrapper">
            <h3>Submit Claim for This Item</h3>
            <p>Please provide detailed justification proving the item is yours. This information will be sent to the item poster (User {item_poster_id}).</p>
            
            <form onSubmit={handleSubmit}>
                <textarea
                    rows="4"
                    placeholder="Describe specific features, time/place of loss, or any unique marks only the owner would know."
                    value={justification}
                    onChange={(e) => setJustification(e.target.value)}
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Submitting...' : 'Confirm Claim'}
                </button>
            </form>
        </div>
    );
};

export default ClaimForm;