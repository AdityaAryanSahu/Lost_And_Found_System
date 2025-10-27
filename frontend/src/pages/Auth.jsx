import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import apiClient from '../api/apiClient';
import './Auth.css';

// Regex for: Min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char
const STRONG_PASSWORD_REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^a-zA-Z0-9]).{8,}$";
const PASSWORD_TITLE = "Must be at least 8 characters and include 1 uppercase, 1 lowercase, 1 number, and 1 special character.";

const AuthPage = () => {
    const navigate = useNavigate();
    const { isAuthenticated, login } = useAuth();  // Use login function from context
    const [isRegister, setIsRegister] = useState(false);
    const [userId, setUserId] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    // Check if already authenticated
    useEffect(() => {
        if (isAuthenticated) {
            navigate('/', { replace: true });
        }
    }, [isAuthenticated, navigate]);

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        try {
            // Step 1: Login and get token
            const loginResponse = await apiClient.post('/auth/login', {
                user_id: userId,
                passwd: password
            });

            const token = loginResponse.data.token;
            
            if (token) {
                // Step 2: Fetch full user profile with email
                try {
                    // Set token temporarily for the next request
                    localStorage.setItem('token', token);
                    
                    // Fetch user profile
                    const profileResponse = await apiClient.get('/users/me');
                    
                    // Create complete user object with email
                    const userData = {
                        user_id: profileResponse.data.user_id || userId,
                        email: profileResponse.data.email || null,
                        username: profileResponse.data.username || null,
                        // Add any other fields from your backend
                    };
                    
                    console.log('Login successful, user data:', userData);
                    
                    // Use login function which saves both token and user
                    login(userData, token);
                    
                    navigate('/', { replace: true });
                    
                } catch (profileError) {
                    console.error('Error fetching profile:', profileError);
                    
                    // Fallback: If profile fetch fails, still login with basic info
                    const basicUserData = {
                        user_id: userId,
                        email: email || null  // Use registration email if available
                    };
                    
                    login(basicUserData, token);
                    navigate('/', { replace: true });
                }
            }
        } catch (error) {
            console.error('Login error:', error);
            setMessage('❌ ' + (error.response?.data?.detail || 'Login failed'));
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        // Frontend check for password complexity before sending (as a double-check)
        // Although the HTML pattern is present, this provides a fallback message.
        const passwordRegexTest = new RegExp(STRONG_PASSWORD_REGEX);
        if (!passwordRegexTest.test(password)) {
            setMessage('❌ ' + PASSWORD_TITLE);
            setLoading(false);
            return;
        }


        try {
            await apiClient.post('/auth/register', {
                username,
                user_id: userId,
                passwd: password,
                email
            });
            
            setMessage('Registration successful! Please login.');
            setIsRegister(false);
            
            // Clear form
            setUsername('');
            setUserId('');
            setPassword('');
            setEmail('');
            
        } catch (error) {
            console.error('Registration error:', error);
            setMessage('❌ ' + (error.response?.data?.detail || 'Registration failed'));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-logo-container">
                    <img 
                        src="/lotandfoundlogo.jpg" 
                        alt="Lost & Found Portal Logo" 
                        className="auth-logo-icon"
                    />
                    <h1 className="auth-title-text">Lost & Found Inventory</h1>
                </div>
                <h2>{isRegister ? 'Register' : 'Login'}</h2>

                {message && (
                    <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
                        {message}
                    </div>
                )}

                <form onSubmit={isRegister ? handleRegister : handleLogin}>
                    {isRegister && (
                        <>
                            <input
                                type="text"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                            />
                            <input
                                type="email"
                                placeholder="Email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </>
                    )}

                    <input
                        type="text"
                        placeholder="User ID"
                        value={userId}
                        onChange={(e) => setUserId(e.target.value)}
                        required
                        autoComplete="username"
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        autoComplete={isRegister ? "new-password" : "current-password"}
                        minLength={isRegister ? "8" : undefined}
                        pattern={isRegister ? STRONG_PASSWORD_REGEX : undefined}
                        title={isRegister ? PASSWORD_TITLE : undefined}
                    />

                    <button type="submit" disabled={loading}>
                        {loading ? 'Loading...' : (isRegister ? 'Register' : 'Login')}
                    </button>
                </form>

                <button
                    type="button"
                    className="toggle-btn"
                    onClick={() => {
                        setIsRegister(!isRegister);
                        setMessage('');  // Clear messages when switching
                    }}
                >
                    {isRegister ? 'Have an account? Login' : 'Need an account? Register'}
                </button>
            </div>
        </div>
    );
};

export default AuthPage;