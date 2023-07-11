import React, { useState } from 'react';
import axios from 'axios';
import './SearchPage.css';
import { useNavigate } from 'react-router-dom';

export const SearchPage = () => {
    const navigate = useNavigate();
    const [value, setSearchQuery] = useState('');
    //const [searchResults, setSearchResults] = useState([]);

    const handleSearch = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.get('/books/search', {
                params: { value },
            });
            console.log(response.data.status_code)
            if (response.data.status_code === 400 || response.data.status_code === 404) {
                alert(response.data.message)
            }
            //setSearchResults(response.data);
            navigate('/book-results', { state: { results: response.data } })
        } catch (error) {
            alert(error.response.data.error);
        }
    };

    return (
        <div className="search">
            <h2 className="search-title">Book Search</h2>
            <div className='search-container'>
                <form onSubmit={handleSearch}>
                    <input
                        className='search-input'
                        type="text"
                        value={value}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                    <button className="search-button" type="submit">Search</button>
                </form>
            </div>
        </div>
    );
}

