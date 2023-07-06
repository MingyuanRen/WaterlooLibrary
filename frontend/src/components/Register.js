import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Register.css';

export const Register = () => {
  const [data, setData] = useState({
    name: '',
    email: '',
    phone: '',
    password: ''
  });

  const navigate = useNavigate();

  const handleChange = e => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const register = async e => {
    e.preventDefault();
    try {
      await axios.post('/register', data);
      alert('New user created!');
      navigate('/homepage'); // redirect to home page
    } catch (error) {
      alert('Error while registering');
    }
  };

  return (
    <div className="container">
      <h1 className="header">Register</h1>
      <form className="register-form" onSubmit={register}>
        <input type='text' name='name' placeholder='Name' className="input-field" onChange={handleChange} required />
        <input type='email' name='email' placeholder='Email' className="input-field" onChange={handleChange} required />
        <input type='tel' name='phone' placeholder='Phone' className="input-field" onChange={handleChange} required />
        <input type='password' name='password' placeholder='Password' className="input-field" onChange={handleChange} required />
        <button type='submit' className="submit-btn">Register</button>
      </form>
    </div>
  );
};
