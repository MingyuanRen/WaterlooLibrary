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

const accountService = {
  findUserInfo,
  getBooksRecords
}

export default accountService