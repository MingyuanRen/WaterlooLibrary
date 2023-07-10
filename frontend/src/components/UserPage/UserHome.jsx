import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Container, Form, Button, Row, Col } from 'react-bootstrap'
import MemberPage from './MemberPage';
import UserProfile from './UserProfile';
import BookRecords from './BookRecords';
import { useSelector } from 'react-redux';
import "./UserHome.css"

const UserHome = () => {
  const location = useLocation();
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Get user from location state and set it to state
    setUser(location.state.user);
  }, [location]);

  const submitHandler = () => {}

  const userRedux = useSelector(state => state.user);

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
                    <li><a className="nametag"><h3>Welcome {user ? user.name : 'Guest'}</h3></a></li>
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
            <UserProfile user={user} />
          }
        {displayMembership && <MemberPage />}
        {displayProfile && <UserProfile user={user} />}
        {displayRecords && <BookRecords user={user} />}
        </Col>
      </Row>
      {/* </div> */}
    </Container>
  );
};

export default UserHome;
