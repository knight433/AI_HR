import React, { useState, useRef, useEffect } from "react";
import "../components/FollowupNode.css";

const FollowupNode = ({ id, content, parentId, onRemove, updateNodeData }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [question, setQuestion] = useState("");
  const [nodeTitle, setNodeTitle] = useState("ADD QUESTION"); // Default text

  const popupRef = useRef(null);

  // Close popup when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (popupRef.current && !popupRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Save and Update Node Title
  const handleSave = () => {
    if (question.trim() !== "") {
      setNodeTitle("Follow Up"); // Update title with question
      updateNodeData(id, question); // Save to parent
    }
    setIsOpen(false);
  };

  return (
    <div className="followup-node-container">
      {/* Small Node Box */}
      <div className="followup-node" id={id} onClick={() => setIsOpen(true)}>
        <button className="remove-btn" onClick={(e) => { e.stopPropagation(); onRemove(id); }}>x</button>
        <h4 className="node-title">{nodeTitle}</h4>
      </div>

      {/* Popup for Editing Node Details */}
      {isOpen && (
        <div className="node-popup" ref={popupRef}>
          <h4>Edit Followup</h4>

          <div className="input-group">
            <label>Question</label>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Enter question"
            />
          </div>

          <div className="popup-buttons">
            <button className="save-btn" onClick={handleSave}>Save</button>
            <button className="close-btn" onClick={() => setIsOpen(false)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FollowupNode;
