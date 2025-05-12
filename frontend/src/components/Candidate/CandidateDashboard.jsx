import { useEffect, useState } from "react";
import axios from "axios";
import './CandidateDashboard.css'
import { toast } from 'react-toastify';

export default function CandidateDashboard() {
    const [profile, setProfile] = useState(null);
    const [editing, setEditing] = useState(false);
    const [updatedData, setUpdatedData] = useState({});
    const token = localStorage.getItem("access_token");
    const DISPLAY_FIELDS = ["email", "full_name", "gender"];
    const FIELD_LABELS = {
        email: "Email",
        full_name: "Full Name",
        gender: "Gender"
    };

    const fetchProfile=async()=>{
        try{
            const response = await axios.get("http://127.0.0.1:8000/api/candidate/me", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            setProfile(response.data.data);
        }catch (error) {
        toast.error("Error fetching profile: " + error.message);
        }
    }

    useEffect(() => {
        fetchProfile();
    }, []);

    const deleteProfile=async()=>{
        if (!window.confirm("Are you sure you want to delete your account?")) return;
        try{
            await axios.delete("http://127.0.0.1:8000/api/candidate/me", {
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

    const updateProfile=async()=>{
        try{
        axios.put("http://127.0.1:8000/api/candidate/me", updatedData, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
        toast.success("Profile updated.");
        setEditing(false);
        fetchProfile();
        }catch (error) {
            toast.error("Error updating profile: " + error.message);
        }
    }

    const logout = () => {
        localStorage.removeItem("access_token");
        window.location.href = "/";
        };

    const handleInputChange=(e)=>{
        setUpdatedData({
            ...updatedData,
            [e.target.name]: e.target.value,
        })
    }

    return (
        <div className="dashboard-container">
            <aside className="sidebar">
                <button
                    onClick={() => {
                    fetchProfile();
                    setEditing(false);
                    }}
                >
                    View Details
                </button>
                <button onClick={() => setEditing(true)}>Update Details</button>
                <button
                    onClick={() => {
                    logout();
                    setEditing(false);
                    }}
                >
                    Logout
                </button>
                <button
                    onClick={() => {
                    deleteProfile();
                    setEditing(false);
                    }}
                    style={{ color: "red" }}
                >
                    Delete Account
                </button>
            </aside>
            <main className="main-content">
                <h1>Candidate Dashboard</h1>
                {editing ? (
                <div>
                    <h2>Update Details</h2>
                    {profile &&
                    DISPLAY_FIELDS.map((field) => (
                        <div key={field}>
                            <label>{FIELD_LABELS[field] || field}</label>
                            {field === "gender" ? (
                                <select name="gender" value={updatedData.gender } onChange={handleInputChange}>
                                    <option value="male">Male</option>
                                    <option value="female">Female</option>
                                    <option value="other">Other</option>
                                </select>
                            ):(
                            <input name={field} value={updatedData[field] || ""} onChange={handleInputChange}/>
                            )}
                        </div>
                    ))}
                    <button onClick={updateProfile}>Save</button>
                    <button onClick={() => setEditing(false)}>Cancel</button>
                </div>
                ) : (
                profile && (
                    <div>
                        <h2>Profile Details</h2>
                        {DISPLAY_FIELDS.map((field) => (
                            <p key={field}>
                            <strong>{FIELD_LABELS[field] || field}:</strong> {profile[field]}
                            </p>
                        ))}
                    </div>
                )
                )}
            </main>
    </div>
);
}


