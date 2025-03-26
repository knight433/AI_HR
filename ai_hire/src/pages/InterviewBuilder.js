import React, { useState } from "react";
import BuildSession from "../components/BuildSession";
import TheorySession from "../components/TheorySession";
import './InterviewBuilder.css'

const InterviewBuilder = () => {
  const [sessions, setSessions] = useState([]);
  const [theoryData, setTheoryData] = useState({});
  const [buildData, setBuildData] = useState({});

  const addBuildSession = () => {
    setSessions([
      ...sessions,
      { id: sessions.length + 1, type: "build", content: `This is Build Session ${sessions.length + 1}` }
    ]);
  };

  const addTheorySession = () => {
    setSessions([
      ...sessions,
      { id: sessions.length + 1, type: "theory", content: `This is Theory Session ${sessions.length + 1}` }
    ]);
  };

  const removeSession = (sessionNumber) => {
    setSessions(sessions.filter((session) => session.id !== sessionNumber));
    setTheoryData((prev) => {
      const updatedData = { ...prev };
      delete updatedData[sessionNumber];
      return updatedData;
    });
    setBuildData((prev) => {
      const updatedData = { ...prev };
      delete updatedData[sessionNumber];
      return updatedData;
    });
  };

  const collectDataAndSend = async () => {
    const formattedTheoryData = Object.values(theoryData).map(session => ({
      sessionNumber: session.sessionNumber,
      nodes: session.nodes.map(node => ({
        id: node.id,
        skill: node.skill || "",
        question: node.question || "",
        level: node.level || 1,
        follow_up: node.type === "followup" ? node.follow_up || "" : "",
      })),
    }));

    const formattedBuildData = Object.values(buildData).map(session => ({
      sessionNumber: session.sessionNumber,
      nodes: session.nodes.map(node => ({
        id: node.id,
        skill: node.skill || "",
        question: node.question || "",
        level: node.level || 1,
        follow_up: node.type === "followup" ? node.follow_up || "" : "",
      })),
    }));

    console.log("Sending Theory Data:", formattedTheoryData);
    console.log("Sending Build Data:", formattedBuildData);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/theory_sessions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ theoryData: formattedTheoryData, buildData: formattedBuildData }),
      });

      const result = await response.json();
      console.log("Response from backend:", result);
    } catch (error) {
      console.error("Error sending data:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Interview Builder</h1>
      <button onClick={addBuildSession} style={{ padding: "10px", margin: "10px" }}>Add Build Session</button>
      <button onClick={addTheorySession} style={{ padding: "10px", margin: "10px" }}>Add Theory Session</button>
      <button onClick={collectDataAndSend} style={{ padding: "10px", margin: "10px", background: "lightblue" }}>Send</button>
      
      <div>
        {sessions.length === 0 ? <p>No sessions added yet</p> : null}
        {sessions.map((session) =>
          session.type === "build" ? (
            <BuildSession
              key={session.id}
              sessionNumber={session.id}
              content={session.content}
              onRemove={removeSession}
              getSessionData={(id, data) => setBuildData(prev => ({ ...prev, [id]: data }))}
            />
          ) : (
            <TheorySession
              key={session.id}
              sessionNumber={session.id}
              content={session.content}
              onRemove={removeSession}
              getSessionData={(id, data) => setTheoryData(prev => ({ ...prev, [id]: data }))}
            />
          )
        )}
      </div>
    </div>
  );
};

export default InterviewBuilder;
