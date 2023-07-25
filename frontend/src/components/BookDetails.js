import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {useLocation} from 'react-router-dom';
import { Link } from "react-router-dom";
import { UserIcon } from "./filter.jsx";
import { motion } from "framer-motion";
import './BookDetails.css';
import bookIcon from './book.png'

export const BookDetails = () => {
    const location = useLocation();
    const [user, setUser] = useState(null);

    let book = location.state.book
    useEffect(() => {
        // Get user from location state and set it to state
        setUser(location.state.user);
      }, [location]);

    const handleBorrow = async (e) => {
        e.preventDefault();
        let email = user.email;
        const user_info = await axios.get('/user', {params: { email }, });
        let uid = user_info.data.uid;

        try {
            const res = await axios.post('/books/borrow', { isbn: book.isbn, uid: uid });
            if (res.data.message === 'Book borrowed successfully') {
                alert(res.data.message);
            }
        } catch (error) {
            alert("Book was not borrowed successfully");
        }
    };
    const handleReserve = async (e) => {
        e.preventDefault();
        let email = user.email;
        const user_info = await axios.get('/user', {params: { email }, });
        let uid = user_info.data.uid;

        try {
            const res = await axios.post('/books/reserve', { isbn: book.isbn, uid: uid });
            alert(res.data.message);
            if (res.data.message === 'Book reserved successfully') {
                alert(res.data.message);
            }
        } catch (error) {
            alert("Book did not get reserved");
        }
    };

    return (
        <motion.div>
        <div>
            <Link to="/user-home" state={{ user: user }}>
                <UserIcon/>
            </Link>
        </div>
        <div className="book-details-container">
      <div className="left-content">
        <div className="book-icon">
          <img src={bookIcon} alt="Book Icon" />
        </div>
        <div className="buttons">
          <button onClick={handleBorrow}>Borrow</button>
          <button onClick={handleReserve}>Reserve</button>
        </div>
      </div>
      <div className="book-details-card">
        <h2>{book.title}</h2>
        <p>Author: {book.author}</p>
        <p>ISBN: {book.isbn}</p>
      </div>
    </div>
    </motion.div>
  );
};