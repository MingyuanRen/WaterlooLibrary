import React from 'react';
import axios from 'axios';

export const BookDetails = ({ book }) => {
    const handleBorrow = async (e) => {
        e.preventDefault();

        try {
            const res = await axios.post('/books/borrow', { bookId: book.isbn })
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
            const res = await axios.post('/books/reserve', { bookId: book.isbn })
            if (res.data.message === 'Book Reserved successfully') {
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