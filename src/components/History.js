// History.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './History.css';

const History = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/users/history/', { withCredentials: true })
      .then(response => {
        setHistory(response.data);
      })
      .catch(error => {
        console.error('Error fetching history:', error);
      });
  }, []);

  return (
    <div className="history-container">
      <h2 className="history-title">Your History</h2>
      <ul className="history-list">
        {history.map((item, index) => (
          <li key={index} className="history-item">
            <div className="history-content">
              <p className="history-function"><strong>Function:</strong> {item.function_str}</p>
              <p className="history-range">
                <strong>x_min:</strong> {item.x_min} | <strong>x_max:</strong> {item.x_max}
              </p>
              <div className="history-chart-container">
                <img src={`data:image/png;base64,${item.chart}`} alt="History Chart" className="history-chart" />
              </div>
              <p className="history-date"><strong>Created At:</strong> {new Date(item.created_at).toLocaleString()}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};


export default History;
