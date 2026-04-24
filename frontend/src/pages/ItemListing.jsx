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
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  
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
  
  // Close dropdown when clicking outside
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
        item.post_type?.toLowerCase().includes(itemStatus)
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

  const badgeGradients = {
    'LOST': 'linear-gradient(135deg, #1C7ED6 0%, #00f2fe 100%)',
    'FOUND': 'linear-gradient(135deg, #D32F2F 0%, #FF5722 100%)'
  };

  return (
    <div className="item-listing-page">
      {/* Top Header Bar */}
      <header className="top-header">
        <div className="header-left">
          <div className="app-logo-container">
            <img 
                src="/lotandfoundlogo.jpg"
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
            <button 
              className="user-avatar" 
              onClick={() => setShowUserMenu(!showUserMenu)}
              title="User Profile"
            >
              {user?.username?.charAt(0).toUpperCase() || 'U'}
            </button>
            
            {showUserMenu && (
              <div className="user-dropdown">
                <div className="user-info">
                  <p className="user-name">{user?.user_id}</p>
                  <p className="user-email">{user?.email || 'user@example.com'}</p>
                </div>
                <hr />
                <button onClick={() => {
                  navigate('/profile');
                  setShowUserMenu(false);
                }}>
                   My Profile
                </button>
                <button onClick={() => {
                  navigate('/my-items');
                  setShowUserMenu(false);
                }}>
                   My Uploads
                </button>
                <button onClick={() => {
                  navigate('/messages');
                  setShowUserMenu(false);
                }}>
                   Messages
                </button>
                <button onClick={() => {
                  navigate('/settings');
                  setShowUserMenu(false);
                }}>
                   Settings
                </button>
                <hr />
                <button 
                  onClick={() => {
                    logout();
                    setShowUserMenu(false);
                  }} 
                  className="logout-btn-dropdown"
                >
                   Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="main-content-wrapper">
        {/* Search & Filter Bar */}
        <div className="search-filter-bar">
          <div className="search-container">
            <span className="search-icon"></span>
            <input
              type="text"
              placeholder="Search items..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
          </div>

          <button
            onClick={() => setShowFilters(!showFilters)}
            className="filters-toggle-btn"
          >
            <span></span>
            Filters
            <span className={`chevron-icon ${showFilters ? 'rotated' : ''}`}>▼</span>
          </button>
        </div>

        {/* Expandable Filters */}
        {showFilters && (
          <div className="filters-expanded">
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

            <div className="filter-section">
              <label>Date From</label>
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="filter-select"
              />
            </div>

            <div className="filter-section">
              <label>Date To</label>
              <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="filter-select"
              />
            </div>

            <div className="filter-section checkbox-section">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={showClaimed}
                  onChange={(e) => setShowClaimed(e.target.checked)}
                />
                <span> Show Claimed Items</span>
              </label>
            </div>

            <button onClick={handleRefresh} className="refresh-btn">
              Reset Filters
            </button>
          </div>
        )}

        {/* Items Grid */}
        <div className="items-main">
          <div className="items-header">
            <h1>Recent Listings [{filteredItems.length}]</h1>
          </div>
          <div className="match-banner" style={{
              background: 'linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%)',
              border: '1px solid #d4af37',
              borderRadius: '10px',
              padding: '20px',
              marginBottom: '30px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
            }}>
              <div>
                <h3 style={{ margin: '0 0 10px 0', color: '#d4af37' }}>Can't find what you're looking for?</h3>
                <p style={{ margin: 0, color: '#ccc' }}>Use our advance matching engine to scan descriptions and locations instantly.</p>
              </div>
              <button 
                onClick={() => navigate('/match')}
                style={{
                  padding: '12px 24px',
                  background: '#d4af37',
                  color: 'black',
                  fontWeight: 'bold',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '16px',
                  transition: 'transform 0.2s'
                }}
                onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
                onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
              >
                Try Smart Match 
              </button>
            </div>

          {loading && <div className="loading">Loading items...</div>}
          {error && <div className="error">{error}</div>}
          
          {!loading && !error && filteredItems.length === 0 && (
            <div className="no-items">No items found</div>
          )}

          <div className="items-grid">
            {filteredItems.map((item) => (
              <div
                key={item.item_id}
                className="item-card"
                data-type={item.type}
                onClick={() => handleItemClick(item.item_id)}
              >
                {/* Image Section */}
                <div className="item-image-container">
                  {item.img && item.img.length > 0 ? (
                    <img src={item.img[0].url} alt={item.desc} className="item-image" />
                  ) : (
                    <div className="no-image">📷 No Image</div>
                  )}
                  
                  {/* Type Badge */}
                  <div 
                    className="item-type-badge"
                    style={{ background: badgeGradients[item.post_type] || badgeGradients['Others'] }}
                  >
                    {item.post_type}
                  </div>

                  {/* Claimed Badge */}
                  {item.is_claimed && (
                    <div className="claimed-badge">
                      ✓ Claimed
                    </div>
                  )}
                </div>

                {/* Item Details */}
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
        </div>
      </div>
    </div>
  );
};

export default ItemListingPage;