import React from 'react';
import axios from 'axios';
import {useLocation} from 'react-router-dom';
import './BookDetails.css';

export const BookDetails = () => {
    const location = useLocation()

    let book = location.state.book
    const user = {"uid": 2}

    const handleBorrow = async (e) => {
        e.preventDefault();

        try {
            const res = await axios.post('/books/borrow', { isbn: book.isbn, uid: user.uid })
            if (res.data.message === 'Book borrowed successfully') {
                alert(res.data.message);
            }
        } catch (error) {
            alert(error.response.data.error);
        }
    };
    const handleReserve = async (e) => {
        e.preventDefault();

        try {
            const res = await axios.post('/books/reserve', { isbn: book.isbn, uid: user.uid })
            alert(res.data.message);
            if (res.data.message === 'Book reserved successfully') {
                alert(res.data.message);
            }
        } catch (error) {
            alert(error.response.data.error);
        }
    };

    return (
        <div className="book-details-container">
            <div className="book-details-card">
                <h2>{book.title}</h2>
                <p>Author: {book.author}</p>
                <p>ISBN: {book.isbn}</p>
                <button onClick={handleBorrow}>Borrow</button>
                <button onClick={handleReserve}>Reserve</button>
            </div>
        </div>
    );
};