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

        console.log("🚨 BUTTON CLICKED! handleSubmit started."); // Add this!
        e.preventDefault();
        
        console.log("Current user state:", user); // Check if user exists
        console.log("Current item_id prop:", item_id);
        setLoading(true);
        onError(null);

        if (!user || !user.user_id) {
            onError("You must be logged in to submit a claim.");
            setLoading(false);
            return;
        }

        // 1. Force everything to a String to perfectly match your ClaimCreation model
        const payload = {
            item_id: String(item_id),
            user_id: String(user.user_id), 
            justification: String(justification),
        };

        // 2. Log exactly what Axios is about to send
        console.log("📤 Sending Claim Payload:", payload);

        try {
            // 3. Add the trailing slash to prevent FastAPI 307 Redirects dropping the body
            await apiClient.post('/claims/', payload);
            
            setLoading(false);
            onSuccess(); 
            
        } catch (error) {
            // 4. Print the EXACT validation error from Pydantic
            console.error("❌ Claim submission failed. FastAPI says:", error.response?.data);
            const detail = error.response?.data?.detail || "Failed to submit claim. Item may be gone.";
            onError(typeof detail === 'string' ? detail : JSON.stringify(detail));
            setLoading(false);
        }
    };

    return (
        <div className="claim-form-wrapper">
            <h3>Submit Claim for This Item</h3>
            <p>Please provide detailed justification proving the item is yours. This information will be sent to the item poster (User {item_poster_id}).</p>
            
            <form>
                <textarea
                    rows="4"
                    placeholder="Describe specific features, time/place of loss, or any unique marks only the owner would know."
                    value={justification}
                    onChange={(e) => setJustification(e.target.value)}
                    required
                />
                <button type="button" 
                    onClick={handleSubmit} 
                    disabled={loading}>
                    {loading ? 'Submitting...' : 'Confirm Claim'}
                </button>
            </form>
        </div>
    );
};

export default ClaimForm;