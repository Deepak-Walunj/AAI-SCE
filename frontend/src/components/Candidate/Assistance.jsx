import React, { useState } from 'react';
import axios from 'axios';
// import './Assistance.css';

export default function Assistant () {
    const [inputText, setInputText] = useState('');
    const [textType, setTextType] = useState('');
    const [tone, setTone] = useState('');
    const [outputType, setOutputType] = useState('');
    const [outputLanguage, setOutputLanguage] = useState('');
    const [result, setResult] = useState('');
    const token = localStorage.getItem("access_token");
    const handleSubmit = async () => {
        try {
        const res = await axios.post("http://127.0.1:8000/api/candidate/process", {
            text: inputText,
            text_type: textType,
            tone: tone,
            output_type: outputType,
            output_language: outputLanguage,
        }, {
            headers: {
                    Authorization: `Bearer ${token}`,
                },
        });
        setResult(res.data.result);
        } catch (err) {
        console.error(err);
        alert("Something went wrong.");
        }
    };

    return (
        <div className="main-container">
            <h1 className="heading">Smart Content Assistant</h1>
            <textarea
                rows={10}
                placeholder="Paste your email, resume, blog post etc..."
                className="textarea"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
            />
            <div className="dropdown">
                <select value={textType} onChange={(e) => setTextType(e.target.value)} className="dropdown-select">
                    <option value="">Select Text Type</option>
                    <option value="email">Email</option>
                    <option value="resume">Resume</option>
                    <option value="blog">Blog</option>
                    <option value="report">Report</option>
                    <option value="social">Social Media Post</option>
                </select>

                <select value={tone} onChange={(e) => setTone(e.target.value)} className="dropdown-select">
                    <option value="">Select Tone</option>
                    <option value="funny">Funny</option>
                    <option value="formal">Formal</option>
                    <option value="persuasive">Persuasive</option>
                    <option value="sarcastic">Sarcastic</option>
                    <option value="motivational">Motivational</option>
                </select>

                <select value={outputType} onChange={(e) => setOutputType(e.target.value)} className="dropdown-select">
                    <option value="">Select Type</option>
                    <option value="summary">Summary</option>
                    <option value="rewrite">Rewritten</option>
                    <option value="personalize">Personalized</option>
                    <option value="style">Style Mimic</option>
                </select>

                <select value={outputLanguage} onChange={(e) => setOutputLanguage(e.target.value)} className='dropdown-select'>
                    <option value="">Select Language</option>
                    <option value="english">English</option>
                    <option value="spanish">Hindi</option>
                    <option value="french">French</option>
                    <option value="german">German</option>
                    <option value="chinese">Chinese</option>
                </select>
            </div>

            <button onClick={handleSubmit} className="output-btn">
                Generate Output
            </button>

            {result && (
                <div className="output-container">
                    <h2 className="font-semibold mb-2">Generated Output:</h2>
                    <p>{result}</p>
                </div>
            )}
        </div>
    );
};

