import React from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import styles from "./AdminHome.module.css";

export const AdminHome = () => {
  const user = useSelector((state) => state.user);
  const [requestsCount, setRequestsCount] = useState(0);

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get("/admin/requestsCount");
      setRequestsCount(response.data.request_num);
    }
    fetchData();
  }, []);

  let navigate = useNavigate();

  const goToAddBook = () => {
    navigate("/admin/addBook");
  };

  const goToReturnBook = () => {
    navigate("/admin/return");
  };

  const goToViewUser = () => {
    navigate("/admin/viewUserInfo");
  };

  const goToRequest = () => {
    navigate("/admin/requests", { state: { user: user } });
  };

  return (
    <div>
      <h1 className={styles.myheader}>
        Hi {user ? user.name : ""}! <br /> Welcome to Waterloo Library Admin
        Home
      </h1>
      <div className={styles.mybuttons}>
        <button className={styles.mybutton} onClick={goToAddBook}>
          Add Book
        </button>
        <button className={styles.mybutton} onClick={goToReturnBook}>
          Return Book
        </button>
        <button className={styles.mybutton} onClick={goToViewUser}>
          View User Info
        </button>
        {/* <p>Number of pending requests: {requestsCount}</p>
        <button className={styles.mybutton} onClick={goToRequest}>Admin Job Requests</button> */}
        <div className={styles.mybuttonContainer}>
          <button className={styles.mybutton} onClick={goToRequest}>
            Job Requests
          </button>
          {requestsCount > 0 && (
            <div className={styles.requestCount}>{requestsCount}</div>
          )}
        </div>
      </div>
    </div>
  );
};
