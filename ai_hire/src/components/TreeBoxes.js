import React, { useState } from "react";
import Xarrow from "react-xarrows";
import "./TreeBoxes.css";

function TreeBoxes() {
  const [boxes, setBoxes] = useState([{ id: "box-1", text: "", parent: null, x: 600, y: 50 }]);

  // Function to add new boxes (1 or 2 children)
  const addBoxes = (parentId, numChildren) => {
    const parent = boxes.find((box) => box.id === parentId);
    const newBoxes = [];

    for (let i = 0; i < numChildren; i++) {
      const newId = `box-${boxes.length + newBoxes.length + 1}`;
      const newX = parent.x + (i === 0 ? -150 : 150); // Place children slightly apart
      const newY = parent.y + 150; // Move children below the parent

      newBoxes.push({ id: newId, text: "", parent: parentId, x: newX, y: newY });
    }

    setBoxes([...boxes, ...newBoxes]);
  };

  // Recursive function to remove a box and all its children
  const removeBoxes = (id) => {
    const removeIds = new Set([id]);

    const findChildren = (parentId) => {
      boxes.forEach((box) => {
        if (box.parent === parentId) {
          removeIds.add(box.id);
          findChildren(box.id);
        }
      });
    };

    findChildren(id);
    setBoxes(boxes.filter((box) => !removeIds.has(box.id)));
  };

  // Handle text change in boxes
  const handleTextChange = (id, newText) => {
    setBoxes(boxes.map((box) => (box.id === id ? { ...box, text: newText } : box)));
  };

  // Send graph to Flask server
  const sendGraphToServer = async () => {
    const graphData = {
      nodes: boxes.map(({ id, text }) => ({ id, text })),
      edges: boxes
        .filter((box) => box.parent !== null)
        .map(({ parent, id }) => ({ from: parent, to: id })),
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/save_graph", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(graphData),
      });

      const result = await response.json();
      console.log("Server Response:", result);
    } catch (error) {
      console.error("Error sending graph:", error);
    }
  };

  return (
    <div>
      <button className="send-graph-button" onClick={sendGraphToServer}>
        Send Graph to Server
      </button>

      <div className="tree-container">
        {boxes.map((box) => (
          <div
            key={box.id}
            id={box.id}
            className="box"
            style={{ left: `${box.x}px`, top: `${box.y}px` }}
          >
            <input
              type="text"
              placeholder="Enter text"
              value={box.text}
              onChange={(e) => handleTextChange(box.id, e.target.value)}
            />
            <div className="button-container">
              <button className="add-button" onClick={() => addBoxes(box.id, 1)}>
                Add One Child
              </button>
              <button className="add-button" onClick={() => addBoxes(box.id, 2)}>
                Add Two Children
              </button>
              <button className="remove-button" onClick={() => removeBoxes(box.id)}>
                Remove
              </button>
            </div>
          </div>
        ))}

        {/* Draw Arrows */}
        {boxes.map((box) =>
          box.parent ? <Xarrow key={`arrow-${box.id}`} start={box.parent} end={box.id} /> : null
        )}
      </div>
    </div>
  );
}

export default TreeBoxes;
