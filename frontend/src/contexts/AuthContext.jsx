import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../api/apiClient';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    // ✅ Load user data from localStorage on mount
    useEffect(() => {
        const loadUser = () => {
            try {
                const token = localStorage.getItem('token');
                const storedUser = localStorage.getItem('user');
                
                if (token && storedUser) {
                    const userData = JSON.parse(storedUser);
                    setUser(userData);
                    setIsAuthenticated(true);
                    console.log('✅ User loaded from localStorage:', userData);
                } else {
                    console.log('❌ No token or user found in localStorage');
                }
            } catch (error) {
                console.error('Error loading user from localStorage:', error);
                // Clear invalid data
                localStorage.removeItem('user');
                localStorage.removeItem('token');
            } finally {
                setIsLoading(false);
            }
        };

        loadUser();
    }, []);

    // ✅ Save user to localStorage whenever it changes
    const updateUser = (userData) => {
        if (userData) {
            setUser(userData);
            setIsAuthenticated(true);
            localStorage.setItem('user', JSON.stringify(userData));
            console.log('✅ User saved to localStorage:', userData);
        }
    };

    // ✅ Login function
    const login = (userData, token) => {
        // Save token
        localStorage.setItem('token', token);
        
        // Save user data
        updateUser(userData);
        
        console.log('✅ Login successful', { userData, token });
    };

    // ✅ Logout function
    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
        setIsAuthenticated(false);
        console.log('✅ Logout successful');
    };

    return (
        <AuthContext.Provider value={{
            user,
            setUser: updateUser,  // ✅ Use updateUser which saves to localStorage
            login,  // ✅ New login function
            updateUser,  // ✅ For profile updates
            isAuthenticated,
            isLoading,
            logout
        }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};
