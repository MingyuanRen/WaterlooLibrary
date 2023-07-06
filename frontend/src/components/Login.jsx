import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setUser } from '../store'; // import the action from your store
import './Login.css';

export const Login = () => {
  const [data, setData] = useState({
    email: '',
    password: '',
  });

  const navigate = useNavigate();
  const dispatch = useDispatch(); // Use useDispatch hook to dispatch actions

  const handleChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const login = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/login', data);
      if (res.data.message === 'Login successful!') {
        alert('Login successful!');
        
        // After successful login, fetch the user's details
        console.log("data", data)
        const userDetails = await axios.get(`http://localhost:8000/user?email=${data.email}`);

        console.log("user:", userDetails.data);
        dispatch(setUser(userDetails.data)); // Dispatch setUser action with the user data from response
  
        navigate('/home'); // redirect to home page
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
