// Navbar.js
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ isAuthenticated,  setIsAuthenticated }) => {
    return (
        <nav className="navbar">
          <div className="navbar-logo">
            <Link to="/" className="logo-link">MyApp</Link>
          </div>
          <div className="navbar-links">
            {isAuthenticated ? (
              <>
                <Link to="/">Interpolation</Link>
                <Link to="/history">History</Link>
                <Link to="/logout" onClick={() => setIsAuthenticated(false)}>Logout</Link>
              </>
            ) : (
              <>
                <Link to="/login">Login</Link>
                <Link to="/register">Register</Link>
              </>
            )}
          </div>
        </nav>
      );
    };

export default Navbar;
