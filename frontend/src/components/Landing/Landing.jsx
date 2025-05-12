import {useNavigate} from 'react-router-dom';

function LandingPage() {
    const navigate= useNavigate();
    return(
        <div className="main-container">
            <div className="info-container">
                <h1>Welcome To Our Platform</h1>
                <p>We are glad to have you here. Please login or register to continue.</p>
            </div>
            <div className="register-button">
                <h3>User Registeration</h3>
                <button className="register-button" onClick={() => navigate('/register')}>Register</button>
            </div>
            <div className="login-button">
                <h3>User Login</h3>
                <button className="login-button" onClick={() => navigate('/login')}>Login</button>
            </div>
            <div className="login-button">
                <h3>Admin Login</h3>
                <button className="login-button" onClick={() => navigate('/admin/login')}>Admin Login</button>
            </div>
        </div> 
    )
}

export default LandingPage;