import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const UserMenu = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (isOpen && !e.target.closest('.user-menu')) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  if (!user) return null;

  const handleMenuClick = (path) => {
    setIsOpen(false);
    navigate(path);
  };

  return (
    <div className="user-menu" style={{ position: 'relative' }}>
      <button 
        className="user-avatar"
        onClick={() => setIsOpen(!isOpen)}
        style={{
          width: '45px',
          height: '45px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
          color: 'white',
          border: 'none',
          fontSize: '18px',
          fontWeight: '700',
          cursor: 'pointer'
        }}
      >
        {user?.user_id?.charAt(0).toUpperCase() || 'U'}
      </button>

      {isOpen && (
        <div style={{
          position: 'absolute',
          right: 0,
          top: '55px',
          background: 'white',
          borderRadius: '8px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.15)',
          minWidth: '220px',
          padding: '12px 0',
          zIndex: 1000
        }}>
          <div style={{ padding: '12px 20px', borderBottom: '1px solid #eee' }}>
            <p style={{ margin: 0, fontWeight: 600, fontSize: '16px' }}>{user.user_id}</p>
            <p style={{ margin: '4px 0 0 0', fontSize: '13px', color: '#666' }}>{user.email || 'user@example.com'}</p>
          </div>

          <button onClick={() => handleMenuClick('/profile')} style={{ width: '100%', padding: '10px 20px', border: 'none', background: 'none', textAlign: 'left', cursor: 'pointer', fontSize: '14px' }}>
            👤 My Profile
          </button>
          
          <button onClick={() => handleMenuClick('/my-items')} style={{ width: '100%', padding: '10px 20px', border: 'none', background: 'none', textAlign: 'left', cursor: 'pointer', fontSize: '14px' }}>
            📋 My Uploads
          </button>

          {/* ✅ ADD MESSAGES BUTTON HERE */}
          <button onClick={() => handleMenuClick('/messages')} style={{ width: '100%', padding: '10px 20px', border: 'none', background: 'none', textAlign: 'left', cursor: 'pointer', fontSize: '14px' }}>
            💬 Messages
          </button>
          
          <button onClick={() => handleMenuClick('/settings')} style={{ width: '100%', padding: '10px 20px', border: 'none', background: 'none', textAlign: 'left', cursor: 'pointer', fontSize: '14px' }}>
            ⚙️ Settings
          </button>

          <div style={{ borderTop: '1px solid #eee', marginTop: '8px', paddingTop: '8px' }}>
            <button onClick={() => { logout(); navigate('/auth'); }} style={{ width: '100%', padding: '10px 20px', border: 'none', background: 'none', textAlign: 'left', cursor: 'pointer', fontSize: '14px', color: '#e74c3c', fontWeight: 600 }}>
              🚪 Logout
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserMenu;
