import React from "react";
import "../components/Session.css";

const BuildSession = ({ sessionNumber, content, onRemove }) => {
  return (
    <div className="session-container">
      <h2>Build Session {sessionNumber}</h2>
      <p>{content}</p>
      <button className="remove-btn" onClick={() => onRemove(sessionNumber)}>Remove</button>
    </div>
  );
};

export default BuildSession;
