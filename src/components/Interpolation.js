// Interpolation.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { refreshToken } from '../utils/auth';
import './Interpolation.css';




const Interpolate = ({ isLoggedIn }) => {
  const [functionInput, setFunctionInput] = useState('');
  const [xMin, setXMin] = useState('');
  const [xMax, setXMax] = useState('');
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState('');
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState(null); // Track task status
  const [isPolling, setIsPolling] = useState(false); // Flag to control polling

  const handleGenerateChart = async () => {
    console.log("start")
    if (!functionInput || !xMin || !xMax) {
      setError('Please fill in all fields.');
      return;
    }

    const tokenRefreshed = await refreshToken();
    if (!tokenRefreshed) {
      alert("Session expired. Please log in again.");
      return;
    }

    try {
      setError('');
      setChartData(null);
      setStatus('pending'); // Set initial status to pending
      setIsPolling(true); // Enable polling

      
      const response = await axios.post(
        'http://localhost:8000/users/generate-chart/',
        { function: functionInput, x_min: xMin, x_max: xMax },
        { withCredentials: true }
      );
      console.log('set request')
      setTaskId(response.data.task_id);
      console.log(response.data.task_id)
    } catch (error) {
      setError('Failed to start chart generation. Please try again.');
      setIsPolling(false); // Stop polling on error
    }
  };

  const handleCancelTask = async () => {
    if (!taskId) return;

    try {
      await axios.post(
        'http://localhost:8000/users/cancel-task/',
        { task_id: taskId },
        { withCredentials: true }
      );
      setStatus('canceled'); // Update status to canceled
      setIsPolling(false); // Stop polling
    } catch (error) {
      setError('Failed to cancel the task. Please try again.');
    }
  };

  // Polling effect to check task status
  useEffect(() => {
    if (isPolling && taskId && status === 'pending') {
      const interval = setInterval(async () => {
        try {
          const response = await axios.get(
            `http://localhost:8000/users/check-task-status/?task_id=${taskId}`,
            { withCredentials: true }
          );

          if (response.data.status === 'pending') {
            console.log(response.data)
            setStatus('pending');
          } else if (response.data.status === 'canceled') {
            console.log('canceled')
            setStatus('canceled');
            setIsPolling(false); // Stop polling if canceled
          } else if (response.data.chart) {
            console.log('done')
            setChartData(response.data.chart);
            setStatus('completed');
            setIsPolling(false); // Stop polling on success
          }
        } catch (error) {
          setError('Error checking task status. Please try again.');
          setIsPolling(false); // Stop polling on error
        }
      }, 2000); // Poll every 2 seconds

      // Cleanup interval on component unmount
      return () => clearInterval(interval);
    }
  }, [isPolling, taskId, status]);

  
  return (
    <div className="interpolation-container">
      <h1 className="title">Function Interpolation</h1>
      <p className="subtitle">Visualize mathematical functions with ease!</p>
      <div className="input-section">
        <label className="label">Enter Function:</label>
        <input
          type="text"
          value={functionInput}
          onChange={(e) => setFunctionInput(e.target.value)}
          placeholder="e.g., x^2 + 3*x + 2"
          className="input-field"
        />
        <label className="label">x Min:</label>
        <input
          type="number"
          value={xMin}
          onChange={(e) => setXMin(e.target.value)}
          placeholder="e.g., -10"
          className="input-field"
        />
        <label className="label">x Max:</label>
        <input
          type="number"
          value={xMax}
          onChange={(e) => setXMax(e.target.value)}
          placeholder="e.g., 10"
          className="input-field"
        />
        <button onClick={handleGenerateChart} className="generate-button">
          Generate Chart
        </button>
        <button
          onClick={handleCancelTask}
          disabled={status !== 'pending'} // Enable only if task is pending
          className="cancel-button"
        >
          Cancel
        </button>
        {error && <p className="error-message">{error}</p>}
      </div>
      {chartData && (
        <div className="chart-section">
          <h2>Generated Chart</h2>
          <img src={`data:image/png;base64,${chartData}`} alt="Interpolation Chart" className="chart-image" />
        </div>
      )}
      {status === 'canceled' && <p className="status-message">Task was canceled.</p>}
      {status === 'completed' && <p className="status-message">Task completed successfully.</p>}
    </div>
  );
};

export default Interpolate;
