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
  return response.data
}

const getBooksRecords = async(userEmail) => {
  let response
  try{
    response = await axios.post(API_URL + '/bookstatus', {"email": userEmail})
  } catch(e){
    console.log(e)
  }
  console.log("after request", userEmail)
  
  if (response.data) {
    localStorage.setItem('bookrecords', JSON.stringify(response.data))
  }
  console.log(response.data)
  return response.data

}


const accountService = {
  findUserInfo,
  getBooksRecords
}

export default accountService