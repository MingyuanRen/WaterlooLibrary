import React from 'react';
import { Link } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import './AdminHome.css';

export const AdminHome = () => {
  return (
    <Container className="custom-container text-center">
      <Row className="justify-content-md-center">
        <Col md="auto">
          <h1 className="title-text">Admin Welcome to WaterlooLibrary!</h1>
          <p className="lead-text">CS 348 Project</p>
        </Col>
      </Row>
      <Row className="justify-content-md-center mt-3">
        <Col md="auto">
          <Link className="btn btn-primary btn-lg custom-button" to="/register">Register</Link>
          <Link className="btn btn-success btn-lg custom-button" to="/login">Login</Link>
        </Col>
      </Row>
    </Container>
  );
};
