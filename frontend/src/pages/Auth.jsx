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
    const { isAuthenticated, login } = useAuth();
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

            const { access_token, refresh_token } = loginResponse.data;
            
            if (access_token) {
                // Step 2: Fetch full user profile with email
                try {
                    // Set token temporarily for the next request
                    localStorage.setItem("access_token", access_token);
                    localStorage.setItem("refresh_token", refresh_token);
                    
                    // Fetch user profile
                    const profileResponse = await apiClient.get('/users/me');
                    console.log(profileResponse.data);
                    // Create complete user object with email
                    const userData = {
                        user_id: profileResponse.data.user_id || userId,
                        email: profileResponse.data.email || null,
                        username: profileResponse.data.username || null,
                    };
                    
                    console.log('Login successful, user data:', userData);
                    
                    // Use login function which saves both token and user
                    login(userData, access_token);
                    
                    navigate('/', { replace: true });
                    
                } catch (profileError) {
                    console.error('Error fetching profile:', profileError);
                    
                    // Fallback: If profile fetch fails, still login with basic info
                    const basicUserData = {
                        user_id: userId,
                        email: email || null
                    };
                    
                    login(basicUserData, access_token);
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

        // Frontend check for password complexity
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
            
            setMessage('✅ Registration successful! Please login.');
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
                {/* Logo Section */}
                <div className="auth-logo-container">
                    <img 
                        src="/lotandfoundlogo.jpg" 
                        alt="Lost & Found Portal Logo" 
                        className="auth-logo-icon"
                    />
                    <h1 className="auth-title-text">Lost & Found Inventory</h1>
                </div>

                {/* Heading */}
                <h2>{isRegister ? 'Create Account' : 'Welcome Back'}</h2>

                {/* Messages */}
                {message && (
                    <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
                        {message}
                    </div>
                )}

                {/* Form */}
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
                                placeholder="Email Address"
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
                        {loading ? 'Processing...' : (isRegister ? 'Create Account' : 'Login')}
                    </button>
                </form>

                {/* Toggle Button */}
                <button
                    type="button"
                    className="toggle-btn"
                    onClick={() => {
                        setIsRegister(!isRegister);
                        setMessage('');
                    }}
                >
                    {isRegister ? '← Back to Login' : 'Create New Account →'}
                </button>
            </div>
        </div>
    );
};

export default AuthPage;