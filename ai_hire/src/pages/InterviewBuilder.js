import React, { useState } from "react";
import BuildSession from "../components/BuildSession";
import TheorySession from "../components/TheorySession";

const InterviewBuilder = () => {
  const [sessions, setSessions] = useState([]);

  const addBuildSession = () => {
    const newSession = {
      id: sessions.length + 1,
      type: "build",
      content: `This is Build Session ${sessions.length + 1}`,
    };
    setSessions([...sessions, newSession]);
  };

  const addTheorySession = () => {
    const newSession = {
      id: sessions.length + 1,
      type: "theory",
      content: `This is Theory Session ${sessions.length + 1}`,
    };
    setSessions([...sessions, newSession]);
  };

  const removeSession = (sessionNumber) => {
    setSessions(sessions.filter((session) => session.id !== sessionNumber));
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Interview Builder</h1>
      <button onClick={addBuildSession} style={{ padding: "10px", margin: "10px" }}>
        Add Build Session
      </button>
      <button onClick={addTheorySession} style={{ padding: "10px", margin: "10px" }}>
        Add Theory Session
      </button>
      <div>
        {sessions.length === 0 ? <p>No sessions added yet</p> : null}
        {sessions.map((session) =>
          session.type === "build" ? (
            <BuildSession
              key={session.id}
              sessionNumber={session.id}
              content={session.content}
              onRemove={removeSession}
            />
          ) : (
            <TheorySession
              key={session.id}
              sessionNumber={session.id}
              content={session.content}
              onRemove={removeSession}
            />
          )
        )}
      </div>
    </div>
  );
};

export default InterviewBuilder;
