import React, { useState } from 'react';
import axios from 'axios';
import styles from './Return.module.css';

function ReturnBook() {
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
      alert(response.data.message);
      // clear the form here
      setRecord({
        email: '',
        isbn: ''
      });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.header}>Return Book</h1>
      <form onSubmit={handleSubmit} className={styles.bookForm}>
        <input type="text" name="isbn" placeholder="ISBN" onChange={handleChange} value={record.isbn}/>
        <input type="email" name="email" placeholder="User Email" onChange={handleChange} value={record.email}/>
        <button type="submit">Return Book</button>
      </form>
    </div>
  );
}

export default ReturnBook;
