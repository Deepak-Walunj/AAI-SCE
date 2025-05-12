import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

function LoginPage({role="candidate"}){
    const navigate=useNavigate()
    const [formData, setFormData]=useState({
        username:"",
        password:"",
        })

        const [token, setToken] = useState(null);

        const handleChange=(e)=>{
            setFormData({
                ...formData,
                [e.target.name]: e.target.value,
            })
        }
        const handleSubmit=async(e)=>{
            e.preventDefault()
        const loginPayload={
            username: formData.username,
            password: formData.password,
            entity_type: role,
        }

        try{
            const response = await axios.post("http://127.0.0.1:8000/api/auth/login", loginPayload, {
                withCredentials: true, 
            });
            const {access_token}=response.data.data;
            setToken(access_token)
            localStorage.setItem("access_token", access_token);
            toast.success("✅ Login successful!");
            if (role==="candidate"){
                navigate('/candidate/dashboard')
            }
            else if (role==="company_admin"){
                navigate('/admin/dashboard')
            }
            else{
                toast.error("❌ Invalid role");
            }
            
        }catch(error){
            if (error.response){
                toast.error("❌ " + error.response.data.detail);
            }
            else if (error.request){
                toast.error("❌ No response from server.");
            }
            else{
                toast.error("❌ Error: " + error.message);
            }
        }
        }
    return(
        <form onSubmit={handleSubmit}>
            <h2>{role === "admin" ? "Admin Login" : "User Login"}</h2>
        
            <input
            type="text"
            name="username"
            placeholder="Email or Username"
            value={formData.username}
            onChange={handleChange}
            required
            /><br/>

            <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
            /><br/>

            <button type="submit">Login</button>
        </form>
    )
}

export default LoginPage;