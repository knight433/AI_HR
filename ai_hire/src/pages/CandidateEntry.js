import React, { useState, useEffect } from "react";
import "./CandidateEntry.css";
import socket from "../socket";

const CandidateEntry = () => {
  const [sessionId, setSessionId] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    // Updated to match backend emit event
    socket.on("session_submit_response", (data) => {
      alert(data.message || "No message from server");
    });

    return () => {
      socket.off("session_submit_response");
    };
  }, []);

  const handleSubmit = () => {
    socket.emit("submit_session", { sessionId, password });
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
