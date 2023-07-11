import React from 'react';
import { useNavigate } from "react-router-dom";
import styles from './Home.module.css';

function Home() {
  let navigate = useNavigate();

  const goToAddBook = () => {
    navigate("/admin/addBook");
  }

  const goToReturnBook = () => {
    navigate("/admin/return")
  }

  const goToViewUser = () => {
    navigate("/admin/viewUserInfo")
  }

  return (
    <div>
      <h1 className={styles.header}>Welcome to the Home Page</h1>
      <div className={styles.buttons}>
        <button className={styles.button} onClick={goToAddBook}>Add Book</button>
        <button className={styles.button} onClick={goToReturnBook}>Return Book</button>
        <button className={styles.button} onClick={goToViewUser}>View User Info</button>
      </div>
    </div>
  );
}

export default Home;
