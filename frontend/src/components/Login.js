import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';

export const Login = () => {
  const [data, setData] = useState({
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const login = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/login', data);
      if (res.data.message === 'Login successful!') {
        alert('Login successful!');
      }
    } catch (error) {
      alert(error.response.data.error);  // Display the error message from the server
    }
  };
  
  
  
  return (
    <div className="container">
      <h1 className="header">Login</h1>
      <form className="login-form" onSubmit={login}>
        <input 
          type="email"
          name="email"
          placeholder="Email"
          className="input-field"
          onChange={handleChange} 
          required 
        />
        <input 
          type="password"
          name="password"
          placeholder="Password"
          className="input-field"
          onChange={handleChange}
          required 
        />
        <button type="submit" className="submit-btn">Login</button>
      </form>
    </div>
  );
};
