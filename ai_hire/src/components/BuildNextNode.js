import React, { useState, useRef, useEffect } from "react";
import "../components/NextNode.css";

const BuildNextNode = ({ id, content, parentId, addFollowup, onRemove, updateNodeData }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [component, setComponent] = useState(""); 
  const [goal, setGoal] = useState("");
  const [level, setLevel] = useState(1);
  const [nodeTitle, setNodeTitle] = useState("ADD COMPONENT"); 

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
    if (component.trim() !== "") {
      setNodeTitle(component);
    }
    setIsOpen(false);
    // Send data to parent
    updateNodeData(id, component, goal, level);
  };

  return (
    <div className="next-node-container">
      <div className="next-node" id={id} onClick={() => setIsOpen(true)}>
        <button className="remove-btn" onClick={(e) => { e.stopPropagation(); onRemove(id); }}>x</button>
        <h4 className="node-title">{nodeTitle}</h4>
      </div>

      {isOpen && (
        <div className="node-popup" ref={popupRef}>
          <h4>Edit Build Node</h4>

          {/* Component Input */}
          <div className="input-group">
            <label>Component</label>
            <input
              type="text"
              value={component}
              onChange={(e) => setComponent(e.target.value)}
              placeholder="Enter component"
            />
          </div>

          {/* Goal Input */}
          <div className="input-group">
            <label>Goal</label>
            <input
              type="text"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="Enter goal"
            />
          </div>

          {/* Level Input */}
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

export default BuildNextNode;
