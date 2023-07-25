import React from 'react';
import { Container, Button, Row, Col } from 'react-bootstrap'
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { reset, adminApply } from '../../states/account/accountSlice'
import { ToastContainer, toast } from 'react-toastify'
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
// import RedeemPage from './RedeemPage';
// import { faBook, faGift, faPiggyBank,faBell, faHeart, faJ, faO, faI, faN, faU, faS, faT, faD, faA, faY } from '@fortawesome/free-solid-svg-icons'
import { Link } from 'react-router-dom';

const AdminApplicationPage = ({ user }) => {
  const dispatch = useDispatch()

  const { isLoading, isSuccess, memberinfo } = useSelector((state) => state.account)
  const [application, setApplication] = useState({
    uid: user.uid,
    reason: ""
  })
  
//   useEffect(() => {
//     if (user && user.email) {
//       dispatch(membershipInfo(user.email))
//     }
//   }, [dispatch, user])

  
  const clickRedeemHandler = (e) => {
    e.preventDefault();
  }

  const clickApplyHandler = (e) => {
    dispatch()
  }

  useEffect(() => {
    console.log("useeffect::", application)
    if ( adminApply ){
      toast.success('Applied Successfully!', {
        position: toast.POSITION.TOP_RIGHT,
      })
    } else {
      toast.error('Application did not go through:(', {
        position: toast.POSITION.TOP_RIGHT,
      })
    }
  },[application])

  if (!user) {
    return <div>Loading user data...</div>;
  }

  if (isLoading) {
    return <div>Loading now...</div>;
  }

  return (
    <div>
        <h1>
            Admin_application
        </h1>
        <br></br>
        <form onSubmit={(e) => {
            e.preventDefault()
            console.log("dispatching adminApply")
            dispatch(adminApply({
                "uid": application.uid,
                "reason": application.reason
            }))
        }}> 
            {/* <input type='text' id='reason' name='reason' onChange={(e) => {
                setApplication({
                    ...application,
                    [e.target.name]: e.target.value,
                })   
            }} /> */}
            <textarea id='reason' name='reason' rows='7' cols='70' onChange={(e) => {
                setApplication({
                    ...application,
                    [e.target.name]: e.target.value,
                })   
            }} placeholder='Provide reasons on why you want to be an administrator! Please keep it short!' />
            <button type="submit">Apply</button>
        </form>
    </div>
  );
}
export default AdminApplicationPage;