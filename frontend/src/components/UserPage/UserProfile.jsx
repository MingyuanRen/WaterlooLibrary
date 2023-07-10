import React from 'react';
import { Container, Button, Row, Col, ListGroup } from 'react-bootstrap'
import { useSelector, useDispatch  } from 'react-redux';
import { useEffect } from 'react';
import { accountInfo, reset } from '../../states/account/accountSlice'
import './UserProfile.css'

const UserProfile = () => {
  const { uid, email, phone, name, isLoading, isSuccess} = useSelector(state => state.account)
  const dispatch = useDispatch()
  
  console.log(uid)
  console.log(email)
  console.log(phone)
  console.log(name)
  console.log(isLoading)
  console.log(isSuccess)

  localStorage.setItem('userEmail', 'lucas@gmail.com')
  const userEmail = localStorage.getItem('userEmail')
  console.log(userEmail)

  useEffect(() => {
    return () => {
      // console.log(isSuccess);
      if (isSuccess) {
        dispatch(reset())
      }
    }
  }, [dispatch, isSuccess])

  
  useEffect(() => {
    if (userEmail) {
      dispatch(accountInfo(userEmail))
    }
  }
  , [dispatch, userEmail])
  
  if (isLoading) {
    // need to be change to a loader component
    return (
      <>
       isLoading now
      </>
    )
  }

  // probably a form would be a good usecase here
  return (
      <div className="text-center">
        <br></br>
        <h2>
          Personal Information
        </h2>
        <br></br>
        <br></br>
          <table class="table">
            <tbody>
              <tr>
                <th scope="row">Name</th>
                <td>{name}</td>
              </tr>
              <tr>
                <th scope="row">Email</th>
                <td>{email}</td>
              </tr>
              <tr>
                <th scope="row">Phone</th>
                <td colspan="2">{phone}</td>
              </tr>
            </tbody>
          </table>
      </div>
  );
};

export default UserProfile;