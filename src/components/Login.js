// Login.js
import React, { useState } from 'react';
import axios from 'axios';
import './Form.css';
import './styles.css';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loginSuccess, setLoginSuccess] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:8000/users/login/', { username, password }, { withCredentials: true });
            setLoginSuccess(true);
        } catch (error) {
            console.error('Login failed', error);
        }
    };

    return (
        <div className="form-container">
          {loginSuccess ? (
            <div>
              <p className='login-success'>Login successful!</p>
              <a href="/" className='ref-success'>Click here to continue</a>
            </div>
          ) : (
            <form onSubmit={handleLogin} className="form">
              <h2 className='login'>Login</h2>
              <label className='label'>Username:</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
              />
              <label className='label'>Password:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
              />
              <button type="submit" className="btn-submit">Login</button>
            </form>
          )}
        </div>
    );
}

export default Login;
