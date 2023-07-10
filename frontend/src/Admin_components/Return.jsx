import React, { useState } from 'react';
import axios from 'axios';
import './Return.css';

function AddBook() {
  const [record, setRecord] = useState({
    email: '',
    isbn: ''
  });

  const handleChange = (e) => {
    setRecord({
      ...record,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/admin/return', record);
      console.log(response.data); // 'success' if everything went well
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="book-form">
      <input type="text" name="isbn" placeholder="ISBN" onChange={handleChange} />
      <input type="email" name="email" placeholder="User Email" onChange={handleChange} />
      <button type="submit">Return Book</button>
    </form>
  );
}

export default AddBook;
