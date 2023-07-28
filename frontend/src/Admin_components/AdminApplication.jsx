import React, { useEffect, useState } from "react";
import axios from "axios";
// import { useSelector } from 'react-redux';
// import styles from "./AdminApplication.module.css"

function Requests() {
  const [requests, setRequests] = useState([]);
  // const user = useSelector(state => state.user);

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get("/admin/requests");
      setRequests(response.data);
    }
    fetchData();
  }, []);

  const handleApprove = async (request) => {
    try {
      const res = await axios.post("/admin/approveRequest", {
        uid: request.uid,
        email: request.email,
      });
      if (res.data.message === "success") {
        alert("Appove successful!");
        setRequests(requests.filter((r) => r.uid !== request.uid));
      }
      //add the code for sending email to the user
    } catch (err) {
      console.error(err);
    }
  };

  const handleDisapprove = async (request) => {
    try {
      const res = await axios.post("/admin/disapproveRequest", {
        uid: request.uid,
        email: request.email,
      });
      if (res.data.message === "success") {
        alert("Disapprove successful!");
        setRequests(requests.filter((r) => r.uid !== request.uid));
      }
      //add the code for sending email to the user
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Applications</h1>
      <br></br>
      {requests.map((request) => (
        <div key={request.rid}>
          <span>Name: {request.name}</span> <span>Email: {request.email}</span>{" "}
          <span>Phone: {request.phone}</span> <br></br>
          <p>Reason: {request.reason}</p>
          <button onClick={() => handleApprove(request)}>Approve</button>
          <button onClick={() => handleDisapprove(request)}>Disapprove</button>
          <hr></hr>
        </div>
      ))}
    </div>
  );
}

export default Requests;
