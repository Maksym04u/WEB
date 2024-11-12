// Register.js
import React, { useState } from 'react';
import axios from 'axios';
import './Form.css';
import './styles.css';

function Register() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [registerSuccess, setRegisterSuccess] = useState(false);

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:8000/users/register/', { username, password }, { withCredentials: true });
            setRegisterSuccess(true);
        } catch (error) {
            console.error('Registration failed', error);
        }
    };

    return (
        <div className="form-container">
          {registerSuccess ? (
            <div>
              <p className='login-success'>Registration successful!</p>
              <a href="/" className='ref-success'>Click here to continue</a>
            </div>
          ) : (
            <form onSubmit={handleRegister} className="form">
              <h2 className='login'>Register</h2>
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
              <button type="submit" className="btn-submit">Register</button>
            </form>
          )}
        </div>
      );
    }
export default Register;
