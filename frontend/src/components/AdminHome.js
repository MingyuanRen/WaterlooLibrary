import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useSelector } from 'react-redux';
import './AdminHome.css';

export const AdminHome = () => {
  const user = useSelector(state => state.user);
  return (
    <Container className="custom-container text-center">
      <Row className="justify-content-md-center">
        <Col md="auto">
          <h1 className="title-text">Hi {user ? user.name : ''}! You are Admin Welcome to WaterlooLibrary!</h1>
        </Col>
      </Row>
    </Container>
  );
};
