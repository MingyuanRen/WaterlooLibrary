import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { Home } from './components/Home';
import { HomePage } from './components/HomePage'; 

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/homepage" element={<HomePage />} />
        <Route path="/home" element={<Home />} />
        {/* Add the following route */}
        <Route path="/" element={<Navigate to="/homepage" />} />
      </Routes>
    </Router>
  );
};

export default App;
