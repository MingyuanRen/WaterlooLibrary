import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Form, Button, Row, Col } from 'react-bootstrap'
import { useState } from 'react';
import MemberPage from './MemberPage';
import UserProfile from './UserProfile';
import BookRecords from './BookRecords';

import "./UserHome.css"

const UserHome = ({ username }) => {
  const submitHandler = () => {}

  const name = "Andrew"
  const email = "andrew@gmail.com"
  const password = "Not showns"
  const confirmPassword = ""

  const [displayProfile, setDisplayProfile ] = useState(false)
  const [displayRecords, setDisplayRecords ] = useState(false)
  const [displayMembership, setDisplayMembership ] = useState(false)

  const clickProfileHandler = (e) => {
    e.preventDefault();

    setDisplayProfile(true)
    setDisplayRecords(false)
    setDisplayMembership(false)
  }
  
  const clickRecordHandler = (e) => {
    e.preventDefault();

    setDisplayProfile(false)
    setDisplayRecords(true)
    setDisplayMembership(false)
  }
  
  const clickMembershipHandler = (e) => {
    e.preventDefault();

    setDisplayProfile(false)
    setDisplayRecords(false)
    setDisplayMembership(true)
  }

  return (
    <Container className="user-home-container">
    {/* <Container fluid> */}
      {/* <div class="row"> */}
      <Row className='align-items-start h-100' style={{ "max-width": "100vw", "width": "100vw"}}>
        <Col md="3" className="left-column">
            <Col>
                <ul>
                <Row>
                    <li><a className="nametag"><h3>Welcome {name}</h3></a></li>
                    {/* <li><a class="active" href="#news">User Profile</a></li>
                    <li><a href="#contact">Books Record</a></li>
                    <li><a href="#about">Membership</a></li>
                    <li><a href="#about">About</a></li> */}
                <Button variant="secondary" onClick={clickProfileHandler}>User Profile</Button>
              </Row>
              <Row>
                <Button variant="secondary" onClick={clickRecordHandler}>Books Record</Button>
              </Row>
              <Row>
                <Button variant="secondary" onClick={clickMembershipHandler}>Membership</Button>
              </Row>
                </ul>
            </Col>
        </Col>
        <Col md="6" className='content-column'>
          {
            !displayMembership && !displayProfile && !displayRecords &&
            <UserProfile />
          }
        {displayMembership && <MemberPage />}
        {displayProfile && <UserProfile />}
        {displayRecords && <BookRecords />}
        </Col>
      </Row>
      {/* </div> */}
    </Container>


  );
};

export default UserHome;