import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setUser } from '../store'; // import the action from your store
import { FaUser, FaEnvelope, FaPhone, FaLock } from 'react-icons/fa';
import './Register.css';


export const Register = () => {
  const [data, setData] = useState({
    name: '',
    email: '',
    phone: '',
    password: ''
  });

  const navigate = useNavigate();
  const dispatch = useDispatch(); // Use useDispatch hook to dispatch actions

  const handleChange = e => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const register = async e => {
    e.preventDefault();
    try {
      const response = await axios.post('/register', data);
      if (response.data.message === 'New user created!') {
        alert(response.data.message);
        dispatch(setUser(data)); // Dispatch setUser action with the original data
        // navigate('/home'); // redirect to home page
        navigate('/search', { state: { user: data } }); // redirect to user home page
      }
    } catch (error) {
      alert('Error while registering');
    }
  };

  return (
    <div className="container">
      <h1 className="header">Register</h1>
      <form className="register-form" onSubmit={register}>
        <div className="input-container">
          <FaUser className="input-icon" />
          <input type='text' name='name' placeholder='Name' className="input-field" onChange={handleChange} required />
        </div>
        <div className="input-container">
          <FaEnvelope className="input-icon" />
          <input name='email' placeholder='Email' className="input-field" onChange={handleChange} required />
        </div>
        <div className="input-container">
          <FaPhone className="input-icon" />
          <input type='tel' name='phone' placeholder='Phone' className="input-field" onChange={handleChange} required />
        </div>
        <div className="input-container">
          <FaLock className="input-icon" />
          <input type='password' name='password' placeholder='Password' className="input-field" onChange={handleChange} required />
        </div>
        <button type='submit' className="submit-btn">Register</button>
      </form>
    </div>
  );
};