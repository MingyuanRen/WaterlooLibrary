import React, { useState } from "react";
import axios from "axios";
import styles from "./AddBook.module.css";

function AddBook() {
  const [book, setBook] = useState({
    isbn: "",
    title: "",
    author: "",
    year_of_publication: "",
    publisher: "",
    inventory: "",
    price: "",
  });

  const handleChange = (e) => {
    setBook({
      ...book,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/admin/addBook", book);
      console.log(response.data); // 'success' if everything went well
      if (response.data.massage === "success") {
        alert("Book added sccessfully!");
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className={styles.addBook_container}>
      <h1 className={styles.addBook_header}>Add Book</h1>
      <form onSubmit={handleSubmit} className={styles.addBook_bookForm}>
        <input
          type="text"
          name="isbn"
          placeholder="ISBN"
          onChange={handleChange}
        />
        <input
          type="text"
          name="title"
          placeholder="Title"
          onChange={handleChange}
        />
        <input
          type="text"
          name="author"
          placeholder="Author"
          onChange={handleChange}
        />
        <input
          type="text"
          name="year_of_publication"
          placeholder="Year of Publication"
          onChange={handleChange}
        />
        <input
          type="text"
          name="publisher"
          placeholder="Publisher"
          onChange={handleChange}
        />
        <input
          type="number"
          name="inventory"
          placeholder="Inventory"
          onChange={handleChange}
        />
        <input
          type="number"
          step="0.01"
          name="price"
          placeholder="Price"
          onChange={handleChange}
        />
        <button type="submit">Add Book</button>
      </form>
    </div>
  );
}

export default AddBook;
