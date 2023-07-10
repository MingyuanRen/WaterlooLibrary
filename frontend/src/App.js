
// import { Register } from './components/Register';
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
// import Home from "./Admin_components/Home"
import Return  from './Admin_components/Return';
import ViewUserInfo from './Admin_components/ViewUserInfo';

const App = () => {
  const [user, setUser] = useState(null);

  return (
    <Router>
      <UserContext.Provider value={{ user, setUser }}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/homepage" element={<HomePage />} />
          <Route path="/home" element={<Home />} />
          <Route path="/admin-home" element={<AdminHome />} />
          {/* Add the following route */}
          <Route path="/" element={<Navigate to="/homepage" />} />
          <Route path="/admin/addBook" element={<AddBook />} />
          <Route path="/admin/return" element={<Return />} />
          <Route path="/admin/viewUserInfo" element={<ViewUserInfo />} />
        </Routes>
      </UserContext.Provider>
    </Router>
  );
};
export default App;
