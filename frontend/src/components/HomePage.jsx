import React from 'react';
import { Link } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import styles from './HomePage.module.css';

export const HomePage = () => {
  return (
    <Container className={styles.customContainer + " text-center"}>
      <Row className="justify-content-md-center">
        <Col md="auto">
          <h1 className={styles.titleText}>Welcome to WaterlooLibrary!</h1>
          <p className={styles.leadText}>CS 348 Project</p>
        </Col>
      </Row>
      <Row className="justify-content-md-center mt-3">
        <Col md="auto">
          <Link className={styles.customButton + " btn btn-primary btn-lg"} to="/register">Register</Link>
          <Link className={styles.customButton + " btn btn-success btn-lg"} to="/login">Login</Link>
        </Col>
      </Row>
    </Container>
  );
};
