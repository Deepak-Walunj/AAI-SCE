import './App.css'
import LandingPage from './components/Landing/Landing';
import UserRegisterationPage from './components/Landing/UserRegisteration';
import LoginPage from './components/Landing/Login'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CandidateDashboard from './components/Candidate/CandidateDashboard';
import AdminDashboard from './components/Admin/AdminDashboard';
import PrivateRoute from './components/PrivateRoute';
import { ToastContainer } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/register" element={<UserRegisterationPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/admin/login" element={<LoginPage role='company_admin'/>} />
          <Route path="/candidate/dashboard" element={<PrivateRoute><CandidateDashboard/></PrivateRoute>} />
          <Route path="/admin/dashboard" element={<PrivateRoute><AdminDashboard/></PrivateRoute>} />
        </Routes>
      </Router>
      <ToastContainer 
          position="top-right" 
          autoClose={2000} 
          hideProgressBar={false} 
          newestOnTop 
          closeOnClick 
          pauseOnHover 
          draggable 
          theme="colored"
      />
    </>
    
  )
}

export default App
