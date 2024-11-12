import axios from 'axios';

export const refreshToken = async () => {
  try {
    const response = await axios.post('http://localhost:8000/users/refresh-token/', {}, { withCredentials: true });
    console.log('Token refreshed successfully:', response.data);
    return true;  // Successfully refreshed
  } catch (error) {
    console.error('Error refreshing token:', error);
    return false;  // Failed to refresh
  }
};
