// Logout.js
import React, { useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Logout.css';


function Logout( {setIsAuthenticated} ) {
    useEffect(() => {
        // Clear the authentication cookie on logout
        const performLogout = async () => {
            try {
                await axios.post('http://localhost:8000/users/logout/', {}, { withCredentials: true });
                setIsAuthenticated(false);
                console.log("Logout successful");
            } catch (error) {
                console.error('Logout failed', error);
            }
        };

        performLogout();
    }, [setIsAuthenticated]);

    return (
        <div className="logout-container">
            <h2 className="logout-message">You have successfully logged out.</h2>
            <Link to="/login" className="logout-link">Click here to log in</Link>
        </div>
    );
}

export default Logout;
