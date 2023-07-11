import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useSelector } from 'react-redux';
import { useNavigate } from "react-router-dom";
import styles from './AdminHome.module.css';

export const AdminHome = () => {
  const user = useSelector(state => state.user);

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
    <Container className="custom-container text-center">
      <Row className="justify-content-md-center">
        <Col md="auto">
          <h1 className={styles.header}>Hi {user ? user.name : ''}! You are Admin Welcome to WaterlooLibrary!</h1>
        </Col>
      </Row>
      <Row className="justify-content-md-center">
        <Col md="auto">
          <button className={`${styles.button} btn btn-primary btn-lg custom-button`} onClick={goToAddBook}>Add Book</button>
        </Col>
      </Row>
      <Row className="justify-content-md-center">
        <Col md="auto">
          <button className={`${styles.button} btn btn-primary btn-lg custom-button`} onClick={goToReturnBook}>Return Book</button>
        </Col>
      </Row>
      <Row className="justify-content-md-center">
        <Col md="auto">
          <button className={`${styles.button} btn btn-primary btn-lg custom-button`} onClick={goToViewUser}>View User Info</button>
        </Col>
      </Row>
    </Container>
  );
};