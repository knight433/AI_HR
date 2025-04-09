import React, { useEffect, useState } from "react";
import Editor from "@monaco-editor/react";
import socket from "../socket";

function CodeEditorWithInstructions() {
  const [instructions, setInstructions] = useState("");

  useEffect(() => {
    // Request instructions from backend
    socket.emit("request_instructions");

    // Listen for response
    socket.on("instructions_data", (data) => {
      setInstructions(data);
    });

    // Cleanup the listener when component unmounts
    return () => {
      socket.off("instructions_data");
    };
  }, []);

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Left Half - Code Editor */}
      <div style={{ flex: 1, borderRight: "1px solid #ccc" }}>
        <Editor
          height="100%"
          defaultLanguage="python"
          defaultValue="# Write your code here"
          theme="vs-dark"
        />
      </div>

      {/* Right Half - Instructions */}
      <div style={{ flex: 1, padding: "20px", overflowY: "auto" }}>
        <h2>Instructions</h2>
        <pre style={{ whiteSpace: "pre-wrap", fontSize: "1rem" }}>
          {instructions}
        </pre>
      </div>
    </div>
  );
}

export default CodeEditorWithInstructions;
