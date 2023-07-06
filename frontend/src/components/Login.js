import React, { useState } from 'react';
import axios from 'axios';

export const Login = () => {
  const [data, setData] = useState({
    email: '',
    password: ''
  });

  const handleChange = e => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const login = async e => {
    e.preventDefault();
    try {
      await axios.post('/login', data);
      alert('Login successful!');
    } catch (error) {
      alert('Invalid username or password');
    }
  };

  return (
    <form onSubmit={login}>
      <input type='email' name='email' placeholder='Email' onChange={handleChange} required />
      <input type='password' name='password' placeholder='Password' onChange={handleChange} required />
      <button type='submit'>Login</button>
    </form>
  );
};
