import React from 'react';
import { useLocation } from 'react-router-dom';
import { Link } from 'react-router-dom';
import './SearchPage.css';

export const BookResults = () => {
    let counter = 1;
    const location = useLocation()
    const mystyle = {
        padding: "20px",
        fontSize: "18px",
        float: "left",
        width: "80%"
    }

    let searchResults = location.state.results

    return (

        <div style={mystyle}>
            <ul className="search-results">
                {
                    searchResults.map((book) => (
                        <tr>
                            <th scope="row">{counter++}</th>
                            <td key={book.isbn}>
                                <Link to={`/books/${book.isbn}`} state={{ book: book }}>{book.title}</Link>
                            </td>
                            <td>{book.author}</td>
                        </tr>
                    ))
                }
            </ul>
        </div>
    );
}

