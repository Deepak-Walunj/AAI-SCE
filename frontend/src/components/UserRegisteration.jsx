import { useState } from 'react';
import axios from 'axios';

const UserRegisterationPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    gender: "male",
    password: "",
  });

  const handleChange = (e) => {
    setFormData(
      { ...formData, [e.target.name]: e.target.value }
    )
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const form = new FormData();
      form.append("name", formData.name);
      form.append("email", formData.email);
      form.append("gender", formData.gender);
      form.append("password", formData.password);

      const response = await axios.post('http://127.0.0.1:8000/api/candidate/register', form);
      alert('Registration successful'+ response.data.message);
      console.log(response.data.data);
    } catch (error) {
      if (error.response) {
        // Server responded with a status outside 2xx
        alert("❌ Error: " + (error.response.data.detail || error.response.data.message));
      } else if (error.request) {
        // Request was made but no response received
        alert("❌ No response from server.");
      } else {
        // Something else
        alert("❌ Error: " + error.message);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
      <input type="text" name='name' placeholder='Full Name' value={formData.name} onChange={handleChange} required/><br />
      <input type="email" name='email' placeholder='Email' value={formData.email} onChange={handleChange} required/><br />
      <input type="password" name='password' placeholder='Password' value={formData.password} onChange={handleChange} required/><br />
      <select name="gender" value={formData.gender} onChange={handleChange} >
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select><br />
      <button type='submit'>Submit</button>
    </form>
  )
};

export default UserRegisterationPage;
