import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { accountInfo } from '../../states/account/accountSlice'
import './UserProfile.css'

const UserProfile = ({ user }) => {

  const dispatch = useDispatch()
  
  useEffect(() => {
    if (user && user.email) {
      dispatch(accountInfo(user.email))
    }
  }, [dispatch, user])
  
  if (!user) {
    return (
      <div>Loading user data...</div>
    );
  }

  return (
    <div className="text-center">
      <br></br>
      <br></br>
      <br></br>
      <br></br>
      <br></br>
      <h2>
        Personal Information
      </h2>
      <br></br>
      <br></br>
      <br></br>
        <table className="table">
          <tbody>
            <tr>
              <th scope="row">Name</th>
              <td>{user.name}</td>
            </tr>
            <tr>
              <th scope="row">Email</th>
              <td>{user.email}</td>
            </tr>
            <tr>
              <th scope="row">Phone</th>
              <td colSpan="2">{user.phone}</td>
            </tr>
          </tbody>
        </table>
    </div>
  );
};

export default UserProfile;
