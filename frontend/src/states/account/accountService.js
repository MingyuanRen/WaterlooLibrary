import axios from 'axios'

const API_URL = '/api/userinfo'

// Register user
const findUserInfo = async (userEmail) => {
  let response
  try{
    response = await axios.post(API_URL + '/account', {"email": userEmail})
  } catch(e){
    console.log(e)
  }
  console.log("after request", userEmail)

  if (response.data) {
    localStorage.setItem('user', JSON.stringify(response.data))
  }
  // console.log(response.data);
  return response.data
}

const membershipInfo = async (userEmail) => {
  let response
  try{
    console.log("run here")
    response = await axios.post(API_URL + '/memberinfo', {"email": userEmail})
    console.log(response.data)
  } catch(e){
    console.log(e)
    throw Error()
  }
  console.log("after request", userEmail)

  if (response.data) {
    localStorage.setItem('membershipInfo', JSON.stringify(response.data))
  }
  // console.log(response.data);
  return response.data
}

// const getBooksRecords = async(uid) => {
//   let response
//   try{
//     response = await axios.post(API_URL + '/bookstatus', {"uid": uid})
//   } catch(e){
//     console.log(e)
//   }
//   console.log("book after request", uid)
  
//   if (response.data) {
//     localStorage.setItem('bookrecords', JSON.stringify(response.data))
//   }
//   console.log(response.data)
//   return response.data

// }
const getBooksRecords = async(uid) => {
  try{
    const response = await axios.post(API_URL + '/bookstatus', {"uid": uid});
    console.log("book after request", response.data);
    return response.data;
  } catch(e){
    console.log(e);
  }
}

const getGiftsList = async(uid) => {
  try{
    const response = await axios.post(API_URL + '/giftlist', {"uid": uid});
    console.log("gifts after request", response.data);
    // debug purpose for putting into localStorage
    localStorage.setItem("gift", response.data)
    return response.data;
  } catch(e){
    console.log(e);
  }
}

const redeem = async(uid, item, points, points_need) => {
  try{
    console.log("redemm::", uid, item, points, points_need)
    const body = {
      "uid": uid, 
      "item": item, 
      "points": points, 
      "points_need": points_need
    }
    const response = await axios.post(API_URL + '/giftlist/redeem', body);
    console.log("redeem...", response.data);
    // debug purpose for putting into localStorage
    localStorage.setItem("redeemable", response.data)
    return response.data.redeemable;
  } catch(e){
    console.log("I should see this")
    console.log(e.message);
    return false
  }
}

const accountService = {
  findUserInfo,
  getBooksRecords,
  membershipInfo,
  getGiftsList,
  redeem
}

export default accountService