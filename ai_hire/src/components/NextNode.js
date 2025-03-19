import React, { useState, useRef, useEffect } from "react";
import "../components/NextNode.css";

const NextNode = ({ id, content, parentId, addFollowup, onRemove, updateNodeData }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [skill, setSkill] = useState(""); 
  const [question, setQuestion] = useState("");
  const [level, setLevel] = useState(1);
  const [nodeTitle, setNodeTitle] = useState("ADD SKILL"); 

  const popupRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (popupRef.current && !popupRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSave = () => {
    if (skill.trim() !== "") {
      setNodeTitle(skill);
    }
    setIsOpen(false);
    // Send data to parent
    updateNodeData(id, skill, question, level);
  };

  return (
    <div className="next-node-container">
      <div className="next-node" id={id} onClick={() => setIsOpen(true)}>
        <button className="remove-btn" onClick={(e) => { e.stopPropagation(); onRemove(id); }}>x</button>
        <h4 className="node-title">{nodeTitle}</h4>
      </div>

      {isOpen && (
        <div className="node-popup" ref={popupRef}>
          <h4>Edit Node</h4>
          <div className="input-group">
            <label>Skill</label>
            <input
              type="text"
              value={skill}
              onChange={(e) => setSkill(e.target.value)}
              placeholder="Enter skill"
            />
          </div>

          <div className="input-group">
            <label>Question</label>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Enter question"
            />
          </div>

          <div className="input-group">
            <label>Level</label>
            <input
              type="number"
              value={level}
              onChange={(e) => setLevel(Math.max(1, Math.min(10, Number(e.target.value))))}
              placeholder="1-10"
              min="1"
              max="10"
            />
          </div>

          <button className="add-followup-btn" onClick={() => addFollowup(id)}>+ Followup</button>
          <div className="popup-buttons">
            <button className="save-btn" onClick={handleSave}>Save</button>
            <button className="close-btn" onClick={() => setIsOpen(false)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default NextNode;
