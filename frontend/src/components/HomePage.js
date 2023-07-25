import React from 'react';
import { Link } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { FaBook, FaUserPlus, FaSignInAlt } from 'react-icons/fa';
import './HomePage.css';
import HomePageImage from '../assets/library.jpg'

export const HomePage = () => {
  return (
    <Container className="custom-container text-center">
      <Row className="justify-content-md-center">
        <Col md="auto">
          <FaBook className="book-icon" />
          <h1 className="title-text">Welcome to WaterlooLibrary!</h1>
          <p className="lead-text">CS 348 Project</p>
          <img src={HomePageImage} className="home-image" alt="Home" />
        </Col>
      </Row>
      <Row className="justify-content-md-center mt-3">
        <Col md="auto">
          <Link className="btn btn-primary btn-lg custom-button" to="/register">
            <FaUserPlus className="icon" /> Register
          </Link>
          <Link className="btn btn-success btn-lg custom-button" to="/login">
            <FaSignInAlt className="icon" /> Login
          </Link>
        </Col>
      </Row>
    </Container>
  );
};
