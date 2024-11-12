// App.js
import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import Login from './components/Login';
import Register from './components/Register';
import Interpolate from './components/Interpolation';
import History from './components/History';
import Logout from './components/Logout'; // Import the new Logout component
import Navbar from './components/Navbar';
import { refreshToken } from './utils/auth';



axios.defaults.withCredentials = true;


const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if the user is authenticated (check if token exists)
    const checkAuthStatus = async () => {
      try {
        const response = await axios.get('http://localhost:8000/users/me/');
        if (response.status === 200) {
          setIsAuthenticated(true);
          console.log(isAuthenticated)

        }
      } catch (err) {
        setIsAuthenticated(false); // If there's an error, the user isn't authenticated
      }
    };

    checkAuthStatus();

  // Set up periodic refresh every 4 minutes
  const interval = setInterval(async () => {
    const refreshed = await refreshToken();
    if (!refreshed) setIsAuthenticated(false);
  }, 4 * 60 * 1000);  // 4 minutes in milliseconds

  return () => clearInterval(interval);  // Clean up interval on unmount

}, []);// Run this effect on initial render

  return (
    <Router>
      <Navbar isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
      <div className="container">
        <Routes>
          <Route
            path="/"
            element={isAuthenticated ? <Interpolate /> : <Navigate to="/login" />}
          />
          <Route
            path="/login"
            element={!isAuthenticated ? <Login /> : <Navigate to="/" />}
          />
          <Route
            path="/register"
            element={!isAuthenticated ? <Register /> : <Navigate to="/" />}
          />
          <Route
            path="/history"
            element={isAuthenticated ? <History /> : <Navigate to="/login" />}
          />
          <Route path="/logout" element={<Logout setIsAuthenticated={setIsAuthenticated} />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;