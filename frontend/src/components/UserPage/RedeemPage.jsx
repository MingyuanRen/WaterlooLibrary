import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getGiftsList, redeem } from '../../states/account/accountSlice';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faStar} from '@fortawesome/free-solid-svg-icons'
import './RedeemPage.css'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'



const RedeemPage = () => {
  const user = JSON.parse(localStorage.getItem("user"))
  const memberinfo = JSON.parse(localStorage.getItem("membershipInfo"))

  const dispatch = useDispatch();
  const { giftsList, isLoading, isSuccess, redeemable } = useSelector((state) => state.account);
  let counter = 1;

  useEffect(() => {
    if (user && user.email && giftsList.length === 0) {
      dispatch(getGiftsList(user.uid));
    }
  }, [dispatch]);

  useEffect(() => {
    console.log("useeffect::", redeemable)
    if ( redeemable ){
      toast.success('Redeemed Successfully!', {
        position: toast.POSITION.TOP_RIGHT,
      })
    } else {
      toast.error('Redeption did not go through:(', {
        position: toast.POSITION.TOP_RIGHT,
      })
    }
  },[redeemable])



  if (!user) {
    return <div>Loading user data...</div>;
  }

  if (isLoading) {
    return <div>Loading now...</div>;
  }
  console.log("giftsList", giftsList);
  return (
    <div className="text-center redeem-container">
      <ToastContainer />
      <br></br>
      <br></br>
      <br></br>
      <br></br>
      <br></br>
      <p style={{"font-size": "50px"}}>
      <FontAwesomeIcon icon={faStar} flip size="2xl" style={{color: "#ffe380",}} />
       POINTS REDEMPTION 
      <FontAwesomeIcon icon={faStar} flip size="2xl" style={{color: "#ffe380",}} />
      </p>
      <br />
      <br></br>
      <br></br>
      <table className="table table-hover w-full text-sm text-left" style={{ width: "50vw", maxWidth: "100%", "font-size": "15px" }}>
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Item</th>
            <th scope="col">Points</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          {giftsList && giftsList.length > 0 && giftsList.map((gift) => (
            <tr key={gift.item}>
              <th scope="row">{counter++}</th>
              <td>{gift.item}</td>
              <td>{gift.point_need}</td>
              <td>
              <button type="button" className="btn btn-outline-success" style={{ "maxWidth": "75px"}} onClick={(e) => {
                e.preventDefault()
                console.log(gift.item)
                dispatch(redeem({
                  "uid": user.uid, 
                  "item": gift.item,
                  "points": memberinfo.memberinfo.points, 
                  "points_need":gift.point_need
                }))
              }}> Redeem </button>
            </td>
            </tr>
          ))}
        </tbody>
      </table>
      {/* {redeemable && <div className="alert alert-success alert-dismissible fade show" role="alert">
                           Success! You have redeem an item!  
                           <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                           </div>}
      {!redeemable && <div className="alert alert-warning alert-dismissible fade show" role="alert"> Sorry, you do not have enough points. </div>}
      <div className="alert alert-warning alert-dismissible fade show" role="alert"> Sorry, you do not have enough points. </div> */}
    </div>
  );
};

export default RedeemPage;