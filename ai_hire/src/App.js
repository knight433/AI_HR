import React from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import InterviewBuilder from "./pages/InterviewBuilder";
import CandidateEntry from "./pages/CandidateEntry";

function HomePage() {
  const navigate = useNavigate();

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Welcome to the App</h1>
      <button onClick={() => navigate("/interview-builder")} style={{ margin: "10px", padding: "10px" }}>
        Go to Interview Builder
      </button>
      <button onClick={() => navigate("/candidate-entry")} style={{ margin: "10px", padding: "10px" }}>
        Go to Candidate Entry
      </button>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/interview-builder" element={<InterviewBuilder />} />
        <Route path="/candidate-entry" element={<CandidateEntry />} />
      </Routes>
    </Router>
  );
}

export default App;
