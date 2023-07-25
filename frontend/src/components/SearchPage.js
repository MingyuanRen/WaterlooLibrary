import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {useLocation} from 'react-router-dom';
import "./newSP.css"; //change CSS file
import { Link } from "react-router-dom";
import { Filter, UserIcon } from "./filter.jsx";
import { motion, AnimatePresence } from "framer-motion";

export const SearchPage = () => {
  let counter = 1;
  const [value, setvalue] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [activeFilter, setActiveFilter] = useState("");
  const [user, setUser] = useState(null);
  const location = useLocation();

  useEffect(() => {
      // Get user from location state and set it to state
      setUser(location.state.user);
    }, [location]);
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
        setSearchResults(response.data);
    } catch (error) {
      alert(error.response.data.error);
    }
  };

  return (
    <motion.div>
        <div>
            <Link to="/user-home" state={{ user: user }}>
                <UserIcon/>
            </Link>
        </div>
      <h2 className="search-title">Book Search</h2>
      <div className="filters">
        <h5 class = "filterText">Search Includes:</h5>
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
              value={value}
              onChange={(e) => setvalue(e.target.value)}
              placeholder="Search a Book..."
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
                !(activeFilter.includes('title')) || book.title.toLowerCase().includes(value.toLowerCase());
              const authorMatch =
                !(activeFilter.includes('author')) || book.author.toLowerCase().includes(value.toLowerCase());
              const isbnMatch = !(activeFilter.includes('isbn')) || book.isbn.includes(value);

              return titleMatch && authorMatch && isbnMatch;
            })
          .map((book) => {
            return (
              <div className="filter-results">
                <scroll className="scroll_table">
                  <div className="return_table">
                  <div className="table_row">
                    <tr>
                      <div className="row_num_cell">
                      <th scope="row" className="row-num">{counter++}</th>
                      </div>
                      <td key={book.isbn} className="return_title">
                        <Link to={`/books/${book.isbn}`} state={{ book: book, user: user }}>
                          {book.title}
                       </Link>
                      </td>
                      <td className="return_author">{book.author}</td>
                    </tr>  
                  </div> 
                  </div>
                </scroll>
              </div>
                
            );
          })}
      </AnimatePresence>
    </motion.div>
  );
};
