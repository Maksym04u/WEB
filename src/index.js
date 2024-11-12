import React from 'react';
import ReactDOM from 'react-dom/client'; // Notice the change here
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root')); // Create the root
root.render(<App />); // Use the `render` method on the root
