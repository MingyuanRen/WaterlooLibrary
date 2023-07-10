import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AddBook  from './Admin_components/AddBook';
import React from 'react';
import Home from "./Admin_components/Home"
import Return  from './Admin_components/Return';
import ViewUserInfo from './Admin_components/ViewUserInfo';
// import { Register } from './components/Register';

const App = () => {
  return (
    <Router>
      <Routes>
        {/* <Route path="/login" element={<Login />} /> */}
        {/* <Route path="/register" element={<Register />} /> */}
        <Route path="/admin/addBook" element={<AddBook />} />
        <Route path="/admin/return" element={<Return />} />
        <Route path="/admin/viewUserInfo" element={<ViewUserInfo />} />
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  );
};
export default App;
