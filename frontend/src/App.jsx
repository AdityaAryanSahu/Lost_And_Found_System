import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import AuthPage from './pages/Auth';
import ItemListingPage from './pages/ItemListing';
import ItemDetailPage from './pages/ItemDetail';
import ItemUploadPage from './pages/ItemUpload';
import ProfilePage from './pages/Profile';
import MyItemsPage from './pages/MyItems';
import SettingsPage from './pages/Settings';
import MessagingPage from './pages/MessagingPage';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }

  return children;
};

function AppRoutes() {
  return (
    <Routes>
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/" element={<Navigate to="/items" replace />} />
      <Route path="/items" element={<ProtectedRoute><ItemListingPage /></ProtectedRoute>} />
      <Route path="/items/:id" element={<ProtectedRoute><ItemDetailPage /></ProtectedRoute>} />
      <Route path="/upload-item" element={<ProtectedRoute><ItemUploadPage /></ProtectedRoute>} />
      
      {/* ADD THESE THREE ROUTES */}
      <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
      <Route path="/my-items" element={<ProtectedRoute><MyItemsPage /></ProtectedRoute>} />
      <Route path="/settings" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />
      
      <Route path="/messages" element={<ProtectedRoute><MessagingPage /></ProtectedRoute>} />
      
      {/* Catch-all - MUST BE LAST */}
      <Route path="*" element={<Navigate to="/items" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;
