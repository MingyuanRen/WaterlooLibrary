import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getBooksRecords, reset, accountInfo } from '../../states/account/accountSlice';

const BookRecords = ({ user }) => {
  const dispatch = useDispatch();
  const { bookRecords, isLoading, isSuccess } = useSelector((state) => state.account);
  let counter = 1;

  useEffect(() => {
    if (user && user.email) {
      dispatch(accountInfo(user.email));
      localStorage.setItem('userEmail', user.email);
      localStorage.setItem('uid', user.uid);
      dispatch(getBooksRecords(user.uid));
    }
  }, [dispatch, user]);

  useEffect(() => {
    if (isSuccess) {
      dispatch(reset());
    }
  }, [dispatch, isSuccess]);

  if (!user) {
    return <div>Loading user data...</div>;
  }

  if (isLoading) {
    return <div>Loading now...</div>;
  }
  console.log("bookRecords", bookRecords);
  return (
    <div className="text-center">
      <br />
      <h2>Unreturned Books</h2>
      <br />
      <br />
      <table className="table table-hover w-full text-sm text-left" style={{ width: "50vw", maxWidth: "100%" }}>
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
          {bookRecords && bookRecords.length > 0 && bookRecords.map((book) => (
            <tr key={book.id}>
              <th scope="row">{counter++}</th>
              <td>{book.title}</td>
              <td>{book.author}</td>
              <td>
                {new Date(book.DateBorrowed).toLocaleDateString('en-US', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                })}
              </td>
              <td>
                {new Date(book.DateDue).toLocaleDateString('en-US', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                })}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BookRecords;
