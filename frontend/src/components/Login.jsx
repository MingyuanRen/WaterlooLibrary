import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setUser } from '../store';
import { FaEnvelope, FaLock } from 'react-icons/fa';
import './Login.css';

export const Login = () => {
  const [data, setData] = useState({
    email: '',
    password: '',
  });

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const login = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/login', data);
      if (res.data.message === 'Login successful!') {
        alert('Login successful!');
        
        const userDetails = await axios.get(`http://localhost:8000/user?email=${data.email}`);
        console.log("user:", userDetails.data);
        dispatch(setUser(userDetails.data));

        if (res.data.is_admin) {
          navigate('/admin-home', { state: { user: userDetails.data } }); // redirect to admin home page
        } else {
          navigate('/search', { state: { user: userDetails.data } }); // redirect to search page
        }
        
      }
    } catch (error) {
      alert(error.response.data.error);
    }
  };

  return (
    <div className="container">
      <h1 className="header">Login</h1>
      <form className="login-form" onSubmit={login}>
        <div className="input-container">
          <FaEnvelope className="input-icon" />
          <input 
            name="email"
            placeholder="Email"
            className="input-field"
            onChange={handleChange} 
            required 
          />
        </div>
        <div className="input-container">
          <FaLock className="input-icon" />
          <input 
            type="password"
            name="password"
            placeholder="Password"
            className="input-field"
            onChange={handleChange}
            required 
          />
        </div>
        <button type="submit" className="submit-btn">Login</button>
      </form>
    </div>
  );
};