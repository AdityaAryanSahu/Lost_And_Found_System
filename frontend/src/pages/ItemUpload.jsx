// src/pages/ItemUpload.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import apiClient from '../api/apiClient';
import './ItemUpload.css';

const ITEM_TYPES = ['Electronics', 'Clothing', 'Books', 'Keys', 'Others'];

const ItemUploadPage = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    
    // Check if we're in edit mode
    const editItemId = searchParams.get('edit');
    const isEditMode = !!editItemId;
    
    const [description, setDescription] = useState('');
    const [itemType, setItemType] = useState('');
    const [images, setImages] = useState([]);
    const [existingImages, setExistingImages] = useState([]); // For edit mode
    const [loading, setLoading] = useState(false);
    const [fetchingItem, setFetchingItem] = useState(false);
    const [errors, setErrors] = useState([]); // Changed to array

    //  Fetch item data if in edit mode
    useEffect(() => {
        if (isEditMode) {
            fetchItemForEdit();
        }
    }, [editItemId]);

    const fetchItemForEdit = async () => {
        setFetchingItem(true);
        try {
            const response = await apiClient.get(`/items/${editItemId}`);
            const item = response.data;
            
            // Pre-fill form with existing data
            setDescription(item.desc || '');
            setItemType(item.type || '');
            setExistingImages(item.img || []);
        } catch (err) {
            console.error('Error fetching item:', err);
            setErrors(['Failed to load item data']);
        } finally {
            setFetchingItem(false);
        }
    };

    const handleFileChange = (e) => {
        const files = Array.from(e.target.files);
        
        if (files.length > 3) {
            setErrors(["Maximum 3 images allowed"]);
            setImages([]);
            return;
        }
        
        setImages(files);
        setErrors([]); //  Clear errors
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors([]); //  Clear previous errors

        // Validation checks
        if (!user) {
            setErrors(["User not authenticated"]);
            return;
        }

        if (!description.trim()) {
            setErrors(["Please provide a description"]);
            return;
        }

        if (!itemType) {
            setErrors(["Please select an item type"]);
            return;
        }

        // For create mode, require at least one image
        // For edit mode, allow no new images if existing images exist
        if (!isEditMode && images.length === 0) {
            setErrors(["Please upload at least one image"]);
            return;
        }

        setLoading(true);

        try {
            const itemDetails = {
                user_id: user.user_id,
                desc: description,
                type: itemType,
            };

            const formData = new FormData();
            formData.append('item_json', JSON.stringify(itemDetails));

            // Append new images if any
            images.forEach((image) => {
                formData.append('image_files', image);
            });

            let response;
            
            if (isEditMode) {
                //  Update existing item (PUT request)
                response = await apiClient.put(`/items/${editItemId}`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
                console.log('Item updated successfully:', response.data);
                alert('Item updated successfully!');
            } else {
                //  Create new item (POST request)
                response = await apiClient.post('/items', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
                console.log('Item posted successfully:', response.data);
                alert('Item posted successfully!');
            }

            // Navigate back to item detail page or home
            if (isEditMode) {
                navigate(`/items/${editItemId}`);
            } else {
                navigate('/');
            }

        } catch (err) {
            console.error("Operation failed:", err.response?.data);
            
            //  PROPER ERROR HANDLING
            const errorDetail = err.response?.data?.detail;
            
            if (Array.isArray(errorDetail)) {
                // Multiple validation errors from FastAPI
                setErrors(errorDetail.map(e => e.msg || String(e)));
            } else if (typeof errorDetail === 'string') {
                // Single error message
                setErrors([errorDetail]);
            } else if (errorDetail && typeof errorDetail === 'object') {
                // Object error (extract msg)
                setErrors([errorDetail.msg || JSON.stringify(errorDetail)]);
            } else {
                // Generic error
                setErrors([`Failed to ${isEditMode ? 'update' : 'upload'} item. Please try again.`]);
            }
        } finally {
            setLoading(false);
        }
    };

    // Show loading while fetching item in edit mode
    if (isEditMode && fetchingItem) {
        return (
            <div className="upload-container">
                <p>Loading item data...</p>
            </div>
        );
    }

    return (
        <div className="upload-container">
            <h2>{isEditMode ? 'Edit Item' : 'Post a Lost or Found Item'}</h2>
            <form onSubmit={handleSubmit} encType="multipart/form-data">
                
                <textarea
                    rows="4"
                    placeholder="Detailed description (color, place found/lost, unique marks)"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                />
                
                <select 
                    value={itemType} 
                    onChange={(e) => setItemType(e.target.value)} 
                    required
                >
                    <option value="">Select Item Type</option>
                    {ITEM_TYPES.map(type => (
                        <option key={type} value={type}>{type}</option>
                    ))}
                </select>

                {/* Show existing images in edit mode */}
                {isEditMode && existingImages.length > 0 && (
                    <div className="existing-images">
                        <p><strong>Current Images:</strong></p>
                        <div className="image-preview-grid">
                            {existingImages.map((img, index) => (
                                <img 
                                    key={index} 
                                    src={img.url} 
                                    alt={`Existing ${index + 1}`}
                                    className="existing-image-preview"
                                />
                            ))}
                        </div>
                        <small>Upload new images to replace current ones</small>
                    </div>
                )}

                <label htmlFor="file-upload" className="file-upload-label">
                    {isEditMode ? 'Upload New Images (Max 3, optional)' : 'Upload Images (Max 3)'}
                </label>
                <input
                    type="file"
                    id="file-upload"
                    multiple
                    accept="image/*"
                    onChange={handleFileChange}
                    required={!isEditMode} // Only required for create mode
                />
                
                {images.length > 0 && <small>{images.length} new file(s) selected.</small>}

                {/*  FIXED ERROR DISPLAY */}
                {errors.length > 0 && (
                    <div className="error-container">
                        {errors.map((error, index) => (
                            <p key={index} className="error-message">{error}</p>
                        ))}
                    </div>
                )}
                
                <button type="submit" disabled={loading || (!isEditMode && images.length === 0)}>
                    {loading ? (isEditMode ? 'Updating...' : 'Uploading...') : (isEditMode ? 'Update Item' : 'Submit Item')}
                </button>
            </form>
            <button onClick={() => navigate(isEditMode ? `/items/${editItemId}` : '/')} className="back-btn">
                Cancel
            </button>
        </div>
    );
};

export default ItemUploadPage;
