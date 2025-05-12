import axios from "axios";
import { useState, useEffect } from "react";
import { toast } from "react-toastify";
import './AdminDashboard.css';

export default function AdminDashboard(){
    const [profile, setProfile] = useState(null);
    const DISPLAY_FIELDS = ["email", "full_name"]
    const FIELD_LABELS = {
        email: "Email",
        full_name: "Full Name",
    };
    const token = localStorage.getItem("access_token");

    const fetchProfile=async()=>{
        try{
            const response = await axios.get("http://127.0.0.1:8000/api/admin/me", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            setProfile(response.data.data);
        }catch(error) {
            toast.error("Error fetching profile: " + error.message);
        }
    }

    useEffect(() => {
        fetchProfile();
    }, []);

    const deleteProfile=async()=>{
        if (!window.confirm("Are you sure you want to delete your account?")) return;
        try{
            await axios.delete("http://127.0.0.1:8000/api/admin/me", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            toast.success("Account deleted.");
            logout();
        }catch (error) {
        toast.error("Error deleting account: " + error.message);
        }
    }

    const logout = () => {  
        localStorage.removeItem("access_token");
        window.location.href = "/";
        };
    return(
        <div className="dashboard-container">
            <aside className="sidebar">
                <button onClick={()=>fetchProfile()}>
                    View Details
                </button>
                <button onClick={()=>logout()}>Logout</button>
                <button onClick={()=>deleteProfile()}>Delete</button>
            </aside>
            <div className="main-content">
                <h1>Admin Dashboard</h1>
                {profile && (
                    <div>
                        <h2>Profile Details</h2>
                        {DISPLAY_FIELDS.map((field) => (
                            <p key={field}>
                            <strong>{FIELD_LABELS[field] || field}:</strong> {profile[field]}
                            </p>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
