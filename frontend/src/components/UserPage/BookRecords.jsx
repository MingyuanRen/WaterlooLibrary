import React from 'react';
import { Container, Button, Row, Col } from 'react-bootstrap'
import { useSelector, useDispatch  } from 'react-redux';
import { useEffect } from 'react';
import { getBooksRecords, reset } from '../../states/account/accountSlice'

const BookRecords = () => {
  const { bookRecords, isLoading, isSuccess} = useSelector(state => state.account)
  const dispatch = useDispatch()
  
  let counter = 1;
  // console.log(bookRecords)
  // console.log(isLoading)
  // console.log(isSuccess)

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
      dispatch(getBooksRecords(userEmail))
    }
  }
  , [dispatch, userEmail])
  
  if (isLoading) {
    return (
      <>
       isLoading now
      </>
    )
  }
  return (
    <div className="text-center">
    <br></br>
      <h2>
        Unreturned Books
      </h2>
      <br></br>
      <br></br>
      <table class="table table-hover w-full text-sm text-left" style={{ "width": "100vw", "max-width": "100%"}}>
        <thead>
            <tr>
            <th scope="col">#</th>
            <th scope="col">Title</th>
            <th scope="col">Author</th>
            <th scope="col">Date Of Borrow</th>
            <th scope="col">Due Date</th>
            </tr>
        </thead>
        <tbody>
    {
      bookRecords.map((book) => (
        <>
        <tr>
            <th scope="row">{counter++}</th>
            <td>{book.author}</td>
            <td>{book.title}</td>
            <td>{new Date(book.DateBorrowed).toLocaleDateString('en-US', {
              day: '2-digit',
              month: '2-digit',
              year: 'numeric',
            })}</td>
            <td>{new Date(book.DateDue).toLocaleDateString('en-US', {
              day: '2-digit',
              month: '2-digit',
              year: 'numeric',
            })}</td>
        </tr>   
        </>
        
      ))
    }
    </tbody>
    </table>
    </div>
  );
};

export default BookRecords;