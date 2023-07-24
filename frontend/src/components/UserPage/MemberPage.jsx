import React from 'react';
import { Container, Button, Row, Col } from 'react-bootstrap'
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { reset, membershipInfo } from '../../states/account/accountSlice'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import RedeemPage from './RedeemPage';
import { faBook, faGift, faPiggyBank,faBell, faHeart, faJ, faO, faI, faN, faU, faS, faT, faD, faA, faY } from '@fortawesome/free-solid-svg-icons'
import { Link } from 'react-router-dom';

const MemberPage = ({ user }) => {
  const dispatch = useDispatch()

  const { isLoading, isSuccess, memberinfo } = useSelector((state) => state.account)
  
  useEffect(() => {
    if (user && user.email) {
      dispatch(membershipInfo(user.email))
    }
  }, [dispatch, user])

  
  const clickRedeemHandler = (e) => {
    e.preventDefault();
  }

  if (!user) {
    return <div>Loading user data...</div>;
  }

  if (isLoading) {
    return <div>Loading now...</div>;
  }
  
  if (!user) {
    return (
      <div>Loading user data...</div>
    );
  }
  const memberInfoFromLocal = JSON.parse(localStorage.getItem("membershipInfo"))
  console.log("memberInfoFromLocal", memberInfoFromLocal)
  if ( memberInfoFromLocal && memberInfoFromLocal.isMember == 'false' ){
    console.log("Here")
    return (
        <div className="text-center">
        <br></br>
        <br></br>
        <br></br>
        <br></br>
        <br></br>
        <h1>
          Membership
        </h1>
        <h7 style={{"color":"grey"}}>CA$11.99/year</h7>
        <br></br>
        <br></br>
        <br></br>
    
        <div>
        <p><FontAwesomeIcon icon={faBook} spin size="2xl" style={{color: "#ff9c66",}} /> Increasing Book Limit From 3 to 5 </p> 
        <p><FontAwesomeIcon icon={faBell} shake size="2xl" style={{color: "#ffdd80",}} />  New Book Reservation Feature </p>     
        <p><FontAwesomeIcon icon={faPiggyBank} bounce size="2xl" style={{color: "#ff9eb6",}} />  Earn 10 Points for Each Borrowing</p>     
        <p><FontAwesomeIcon icon={faGift} flip size="xl" style={{color: "#a76ffb",}} />  Gift Redeemption Avaliable Now</p> 
        <br></br>
        <br></br>
        
        <p>
        <FontAwesomeIcon icon={faHeart} beatFade size="2xl" style={{color: "#ff0000",}} className='fa-fw' />
        <FontAwesomeIcon icon={faHeart} beatFade size="2xl" style={{color: "#ff0000",}} />
        <FontAwesomeIcon icon={faHeart} beatFade size="2xl" style={{color: "#ff0000",}} />
    
        <FontAwesomeIcon icon={faJ} beatFade size="2xl" style={{color: "#4725f4",}} />
        <FontAwesomeIcon icon={faO} beatFade size="2xl" style={{color: "#2465ff",}} />
        <FontAwesomeIcon icon={faI} beatFade size="2xl" style={{color: "#33f1ff",}} />
        <FontAwesomeIcon icon={faN} beatFade size="2xl" style={{color: "#2effc0", marginRight: "20px",}} />
    
        <FontAwesomeIcon icon={faU} beatFade size="2xl" style={{color: "#43d457",}} />
        <FontAwesomeIcon icon={faS} beatFade size="2xl" style={{color: "#adfa1e", marginRight: "20px",}} />
        
        <FontAwesomeIcon icon={faT} beatFade size="2xl" style={{color: "#ffe14d",}} />
        <FontAwesomeIcon icon={faO} beatFade size="2xl" style={{color: "#ffbc05",}} />
        <FontAwesomeIcon icon={faD} beatFade size="2xl" style={{color: "#ff7300",}} />
        <FontAwesomeIcon icon={faA} beatFade size="2xl" style={{color: "#ff4242",}} />
        <FontAwesomeIcon icon={faY} beatFade size="2xl" style={{color: "#ff57c1",}} />
        
        <FontAwesomeIcon icon={faHeart} beatFade size="2xl" style={{color: "#ff0000",}} />
        <FontAwesomeIcon icon={faHeart} beatFade size="2xl" style={{color: "#ff0000",}} />
        <FontAwesomeIcon icon={faHeart} beatFade size="2xl" style={{color: "#ff0000",}} />
        </p>
        
        </div>
    
        <br></br>
        <br></br>
          
      </div>
    );

  } else if (memberInfoFromLocal && memberInfoFromLocal.isMember == 'true') {
    console.log(memberInfoFromLocal)
    return (
      <>

      <div className="text-center">
      <br></br>
      <br></br>
      <br></br>
      <h2>
        Membership Information
      </h2>
      <br></br>
      <br></br>
        <table className="table">
          <tbody>
            <tr>
              <th scope="row">mID</th>
              <td>{memberInfoFromLocal.memberinfo.mID}</td>
            </tr>
            <tr>
              <th scope="row">points</th>
              <td>{memberInfoFromLocal.memberinfo.points}</td>
            </tr>
            <tr>
              <th scope="row">Start Date</th>
              <td colSpan="2">
                {new Date(memberInfoFromLocal.memberinfo.start_date).toLocaleDateString('en-US', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                })}
              </td>
            </tr>
            <tr>
              <th scope="row">End Date</th>
              <td colSpan="2">
                {new Date(memberInfoFromLocal.memberinfo.end_date).toLocaleDateString('en-US', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                })}
              </td>
            </tr>
          </tbody>
        </table>
    </div>
    <br></br>
    <br></br>
    <div className="d-grid gap-2 d-md-flex justify-content-md-end">
      <Link to='/redeem' className='btn btn-outline-info'>
        {/* <button className="btn btn-outline-info" type="button" onClick={clickRedeemHandler}> */}
          Redeem Points
        {/* </button> */}
      </Link>
    </div>
    {/* {displayRedeem && <RedeemPage user={user} />} */}
    </>
    )
  } else {
    console.log(memberinfo)
    return (
      <>Loading Member Info...</>
    )
  }
};

export default MemberPage;