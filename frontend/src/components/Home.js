import React from 'react';
import { Link } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export const Home = () => {
  return (
    <Container className="mt-5 text-center">
      <Row className="justify-content-md-center">
        <Col md="auto">
          <h1>Welcome to WaterlooLibrary!</h1>
          <p className="lead">CS 348 Project</p>
        </Col>
      </Row>
      <Row className="justify-content-md-center mt-3">
        <Col md="auto">
          <Link className="btn btn-primary btn-lg mr-2" to="/register">Register</Link>
          <Link className="btn btn-success btn-lg" to="/login">Login</Link>
        </Col>
      </Row>
    </Container>
  );
};
