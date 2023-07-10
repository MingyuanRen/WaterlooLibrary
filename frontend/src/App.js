import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { Home } from './components/Home';
import { HomePage } from './components/HomePage'; 
import { AdminHome } from './components/AdminHome';
import { SearchPage } from './components/SearchPage';
import React, { useState } from 'react';
import { UserContext } from './UserContext';

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
          <Route path="/search" element={<SearchPage />} />
          {/* Add the following route */}
          <Route path="/" element={<Navigate to="/homepage" />} />
        </Routes>
      </UserContext.Provider>

    </Router>
  );
};

export default App;
