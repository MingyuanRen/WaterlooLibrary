import React, { useState } from "react";
import axios from "axios";
import "./SearchPage.css";
import { Link } from "react-router-dom";
import { Filter, UserIcon } from "./filter.jsx";
import { motion, AnimatePresence } from "framer-motion";

export const SearchPage = () => {
  let counter = 1;
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [activeFilter, setActiveFilter] = useState("");

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      /*
            const response = await axios.get('/books/search', {
                params: { value },
            });
            console.log(response.data.status_code)
            if (response.data.status_code === 400 || response.data.status_code === 404) {
                alert(response.data.message)
            }
            setSearchResults(response.data);*/
      setSearchResults([{ isbn: "123456789", title: "fake_title" , author: "a"}]);
    } catch (error) {
      alert(error.response.data.error);
    }
  };

  return (
    <motion.div>
        <div>
            <Link to="/user-home">
                <UserIcon/>
            </Link>
        </div>
      <div className="search">
        <h2 className="search-title">Book Search</h2>
      </div>
      <div className="filters">
      <Filter
          title="Title"
          isActive={activeFilter.includes('title')}
          onClick={() =>
            setActiveFilter((prevFilters) =>
              prevFilters.includes('title')
                ? prevFilters.filter((filter) => filter !== 'title')
                : [...prevFilters, 'title']
            )
          }
        />
        <Filter
          title="Author"
          isActive={activeFilter.includes('author')}
          onClick={() =>
            setActiveFilter((prevFilters) =>
              prevFilters.includes('author')
                ? prevFilters.filter((filter) => filter !== 'author')
                : [...prevFilters, 'author']
            )
          }
        />
        <Filter
          title="ISBN"
          isActive={activeFilter.includes('isbn')}
          onClick={() =>
            setActiveFilter((prevFilters) =>
              prevFilters.includes('isbn')
                ? prevFilters.filter((filter) => filter !== 'isbn')
                : [...prevFilters, 'isbn']
            )
          }
        />
      </div>
      <div className="search">
        <div className="search-container">
          <form onSubmit={handleSearch}>
            <input
              className="search-input"
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button className="search-button" type="submit">
              Search
            </button>
          </form>
          
        </div>
      </div>
      <AnimatePresence>
      {searchResults
            ?.filter((book) => {
              const titleMatch =
                !(activeFilter.includes('title')) || book.title.toLowerCase().includes(searchQuery.toLowerCase());
              const authorMatch =
                !(activeFilter.includes('author')) || book.author.toLowerCase().includes(searchQuery.toLowerCase());
              const isbnMatch = !(activeFilter.includes('isbn')) || book.isbn.includes(searchQuery);

              return titleMatch && authorMatch && isbnMatch;
            })
          .map((book) => {
            return (
                <scroll>
                  <tr>
                <th scope="row">{counter++}</th>
                <td key={book.isbn}>
                  <Link to={`/books/${book.isbn}`} state={{ book: book }}>
                    {book.title}
                  </Link>
                </td>
                <td>{book.author}</td>
              </tr>  
                </scroll>
            );
          })}
      </AnimatePresence>
    </motion.div>
  );
};
