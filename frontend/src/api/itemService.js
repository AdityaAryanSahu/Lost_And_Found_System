import apiClient from './apiClient';

export const getItems = async (filters = {}) => {
  try {
    const response = await apiClient.get('/items/', { params: filters });
    return response.data;
  } catch (err) {
    console.error("Failed to fetch items:", err);
    throw err;
  }
};

export const getItemDetails = async (itemId) => {
  try {
    const response = await apiClient.get(`/items/${itemId}`);
    return response.data;
  } catch (err) {
    console.error("Failed to fetch item details:", err);
    throw err;
  }
};

export const createItem = async (itemData, images) => {
  try {
    const formData = new FormData();
    formData.append('item_json', JSON.stringify(itemData));
    images.forEach(img => formData.append('image_files', img));
    
    const response = await apiClient.post('/items', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  } catch (err) {
    console.error("Failed to create item:", err);
    throw err;
  }
};