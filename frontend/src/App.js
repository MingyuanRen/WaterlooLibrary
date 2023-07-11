import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { Home } from './components/Home';
import { HomePage } from './components/HomePage'; 
import { AdminHome } from './components/AdminHome';
import React, { useState } from 'react';
import { UserContext } from './UserContext';
import AddBook  from './Admin_components/AddBook';
import Return  from './Admin_components/Return';
import ViewUserInfo from './Admin_components/ViewUserInfo';
import UserHome from './components/UserPage/UserHome';
import UserProfile from './components/UserPage/UserProfile'
import BookRecords from './components/UserPage/BookRecords'

const App = () => {
  const [user, setUser] = useState(null);

  return (
    <Router>
      {/* <main className="py-3"> */}
      <UserContext.Provider value={{ user, setUser }}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/homepage" element={<HomePage />} />
          <Route path="/admin/addBook" element={<AddBook />} />
          <Route path="/admin/return" element={<Return />} />
          <Route path="/admin/viewUserInfo" element={<ViewUserInfo />} />
          <Route path="/home" element={<Home />} />
          <Route path="/admin-home" element={<AdminHome />} />
          <Route path="/user-home" element={<UserHome />} />
          <Route path="/user-profile" element={<UserProfile />} />
          <Route path="/bookrecords" element={<BookRecords />} />
          {/* Add the following route */}
          <Route path="/" element={<Navigate to="/homepage" />} />
        </Routes>
      </UserContext.Provider>
      {/* </main> */}
    </Router>
  );
};

export default App;
