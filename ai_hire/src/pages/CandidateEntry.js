import React, { useState } from "react";
import "./CandidateEntry.css";

const CandidateEntry = () => {
  const [sessionId, setSessionId] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://localhost:5000/submit-session", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sessionId, password }),
      });

      const data = await response.json();
      if (response.ok) {
        alert("Session submitted successfully!");
      } else {
        alert(data.message || "Submission failed");
      }
    } catch (error) {
      alert("Error sending data to the backend.");
      console.error(error);
    }
  };

  return (
    <div className="candidate-entry-container">
      <h1>Candidate Entry</h1>
      <p>Welcome to the Candidate Entry Page!</p>

      <div className="form-group">
        <label>Session ID:</label>
        <input
          type="text"
          value={sessionId}
          onChange={(e) => setSessionId(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <button onClick={handleSubmit}>Send</button>
    </div>
  );
};

export default CandidateEntry;
