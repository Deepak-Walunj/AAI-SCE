import './App.css'
import LandingPage from './components/Landing';
import UserRegisterationPage from './components/UserRegisteration';
import LoginPage from './components/Login'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/register" element={<UserRegisterationPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/admin/login" element={<AdminLoginPage role='company_admin'/>} />
      </Routes>
    </Router>   
  )
}

export default App
