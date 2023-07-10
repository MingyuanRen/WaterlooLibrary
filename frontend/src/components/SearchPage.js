import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './SearchPage.css';

export const SearchPage = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);

    const handleSearch = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.get('/books/search', {
                params: { query: searchQuery },
            });
            setSearchResults(response.data);
        } catch (error) {
            alert(error.response.data.error);
        }
    };

    return (
        <div className="search-container">
            <h2 className="search-title">Book Search</h2>
            <form onSubmit={handleSearch}>
                <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button className="search-button" type="submit">Search</button>
            </form>

            <ul className="search-results">
                {searchResults.map((book) => (
                    <li key={book.id}>
                        <Link to={`/books/${book.isbn}`}>{book.title}</Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default SearchPage;
