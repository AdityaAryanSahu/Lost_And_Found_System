import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import apiClient from '../api/apiClient';
import './ItemListing.css';

const ItemListingPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [filteredItems, setFilteredItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showUserMenu, setShowUserMenu] = useState(false); // ✅ ADDED
  
  // Filter states
  const [searchQuery, setSearchQuery] = useState('');
  const [itemType, setItemType] = useState('all');
  const [showClaimed, setShowClaimed] = useState(false);
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [itemStatus, setItemStatus] = useState('all');
  
  useEffect(() => {
    fetchItems();
  }, []);
  
  // Apply filters whenever any filter changes
  useEffect(() => {
    applyFilters();
  }, [searchQuery, itemType, showClaimed, dateFrom, dateTo, itemStatus, items]);
  
  // ✅ ADDED - Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showUserMenu && !event.target.closest('.user-menu')) {
        setShowUserMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showUserMenu]);
  
  const fetchItems = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/items/');
      setItems(response.data.item_list || []);
      setError(null);
    } catch (err) {
      console.error("Failed to fetch items:", err);
      setError("Could not load items. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  
  const applyFilters = () => {
    let filtered = items;
    
    // Search query filter
    if (searchQuery) {
      filtered = filtered.filter(item =>
        item.desc?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.type?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    // Item type filter
    if (itemType !== 'all') {
      filtered = filtered.filter(item => item.type === itemType);
    }
    
    // Claimed status filter
    if (!showClaimed) {
      filtered = filtered.filter(item => !item.is_claimed);
    }
    
    // Lost/Found status filter
    if (itemStatus !== 'all') {
      filtered = filtered.filter(item => 
        item.desc?.toLowerCase().includes(itemStatus)
      );
    }
    
    // Date from filter
    if (dateFrom) {
      filtered = filtered.filter(item => {
        const itemDate = new Date(item.created_at);
        const fromDate = new Date(dateFrom);
        return itemDate >= fromDate;
      });
    }
    
    // Date to filter
    if (dateTo) {
      filtered = filtered.filter(item => {
        const itemDate = new Date(item.created_at);
        const toDate = new Date(dateTo);
        toDate.setHours(23, 59, 59, 999);
        return itemDate <= toDate;
      });
    }
    
    setFilteredItems(filtered);
  };
  
  const handleRefresh = () => {
    setSearchQuery('');
    setItemType('all');
    setShowClaimed(false);
    setDateFrom('');
    setDateTo('');
    setItemStatus('all');
    fetchItems();
  };
  
  const handleItemClick = (itemId) => {
    navigate(`/items/${itemId}`);
  };

  return (
    <div className="app-container">
      {/* Top Header Bar */}
      <header className="top-header">
        <div className="header-left">
          <div className="app-logo-container">
            <img 
                src="/lotandfoundlogo.jpg" // <<< CRITICAL: Update this path 
                alt="Lost & Found Portal Logo" 
                className="app-logo-icon"
            />
            <h1 className="app-title">Lost & Found Inventory</h1>
          </div>
          </div>
        
        <div className="header-center">
          <button 
            className="post-item-btn"
            onClick={() => navigate('/upload-item')}
          >
             Post New Item
          </button>
        </div>
        
        <div className="header-right">
          <div className="user-menu">
            <button className="user-avatar" onClick={() => setShowUserMenu(!showUserMenu)}>
              {user?.user_id?.charAt(0).toUpperCase() || 'U'}
            </button>
            
                            {showUserMenu && (
                <div className="user-dropdown">
                    <div className="user-info">
                    <p className="user-name">{user?.user_id}</p>
                    <p className="user-email">{user?.email || 'user@example.com'}</p>
                    </div>
                    <hr />
                    <button onClick={() => navigate('/profile')}>
                     My Profile
                    </button>
                    <button onClick={() => navigate('/my-items')}>
                     My Uploads
                    </button>
                    {/*  ADD THIS LINE */}
                    <button onClick={() => navigate('/messages')}>
                     Messages
                    </button>
                    <button onClick={() => navigate('/settings')}>
                     Settings
                    </button>
                    <hr />
                    <button onClick={logout} className="logout-btn-dropdown">
                     Logout
                    </button>
                </div>
                )}
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="item-listing-page">
        {/* Filter Sidebar */}
        <aside className="filters-sidebar">
          <div className="filters-header">
            <h2>Filters</h2>
          </div>
          
          {/* Search Box */}
          <div className="filter-section">
            <label>Search</label>
            <input
              type="text"
              placeholder="Search items..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
          </div>
          
          {/* Lost/Found Status */}
          <div className="filter-section">
            <label>Status</label>
            <select
              value={itemStatus}
              onChange={(e) => setItemStatus(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Items</option>
              <option value="lost">Lost</option>
              <option value="found">Found</option>
            </select>
          </div>
          
          {/* Item Type */}
          <div className="filter-section">
            <label>Item Type</label>
            <select
              value={itemType}
              onChange={(e) => setItemType(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Types</option>
              <option value="Books">Books</option>
              <option value="Electronics">Electronics</option>
              <option value="Clothing">Clothing</option>
              <option value="Keys">Keys</option>
              <option value="Others">Others</option>
            </select>
          </div>
          
          {/* Date Range */}
          <div className="filter-section">
            <label>Date From</label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="date-input"
            />
          </div>
          
          <div className="filter-section">
            <label>Date To</label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="date-input"
            />
          </div>
          
          {/* Show Claimed Items */}
          <div className="filter-section">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={showClaimed}
                onChange={(e) => setShowClaimed(e.target.checked)}
              />
              <span>Show Claimed Items</span>
            </label>
          </div>
          
          {/* Refresh Button */}
          <button onClick={handleRefresh} className="refresh-btn">
             Refresh
          </button>
        </aside>
        
        {/* Items Grid */}
        <main className="items-main">
          <div className="items-header">
            <h1>Recent Listings ({filteredItems.length})</h1>
          </div>
          
          {loading && <p>Loading items...</p>}
          {error && <div className="error-message">{error}</div>}
          
          <div className="items-grid">
            {filteredItems.map((item) => (
              <div
                key={item.item_id}
                className="item-card"
                data-type={item.type}
                onClick={() => handleItemClick(item.item_id)}
              >
                {/* Type Badge */}
                <div className="item-type-badge">{item.type}</div>
                
                {/* Image */}
                {item.img && item.img.length > 0 ? (
                  <img src={item.img[0].url} alt={item.desc} className="item-image" />
                ) : (
                  <div className="no-image">📷 No Image</div>
                )}
                
                {/* Item Details */}
                <div className="item-details">
                  <h3>{item.type}</h3>
                  <div className="item-meta">
                    <p>📍 {item.desc}</p>
                    <p>📅 {new Date(item.created_at).toLocaleDateString()}</p>
                    <p className={item.is_claimed ? 'status-claimed' : 'status-available'}>
                      {item.is_claimed ? ' Claimed' : ' Available'}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
};

export default ItemListingPage;
