// api.js —  backend API calls are here
// Local : http://localhost:5000/api
// after deployment we can add url


const BASE = 'https://voltverse.onrender.com/api';

async function apiCall(path, method = 'GET', body = null) {
  try {
    const options = {
      method,
      headers: { 'Content-Type': 'application/json' }
    };
    if (body) options.body = JSON.stringify(body);
    const res = await fetch(BASE + path, options);
    return await res.json();
  } catch (err) {
    console.error('API Error:', err);
    return { error: 'Unable to connect to server. Please try again.' };
  }
}

// Auth
const loginUser    = (email, password) => apiCall('/auth/login', 'POST', { email, password });
const registerUser = (data)            => apiCall('/auth/register', 'POST', data);

// Stations
const getStations  = ()   => apiCall('/stations/');
const getStation   = (id) => apiCall(`/stations/${id}`);

// Slots
const getAvailableSlots = (stationId, date) =>
  apiCall(`/bookings/available?station_id=${stationId}&date=${date}`);

// Bookings
const createBooking  = (data) => apiCall('/bookings/', 'POST', data);
const getUserBookings = (userId) => apiCall(`/bookings/user/${userId}`);
const cancelBooking  = (id) => apiCall(`/bookings/${id}/cancel`, 'PATCH');
