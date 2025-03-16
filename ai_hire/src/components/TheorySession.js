import React, { useState, useEffect } from "react";
import NextNode from "../components/NextNode";
import FollowupNode from "../components/FollowupNode";
import Xarrow, { useXarrow } from "react-xarrows";
import "../components/Session.css";

const TheorySession = ({ sessionNumber, content, onRemove }) => {
  const [nodes, setNodes] = useState([]);
  const updateXarrow = useXarrow();

  useEffect(() => {
    updateXarrow(); // Refresh arrows when nodes change
  }, [nodes, updateXarrow]);

  const addNext = () => {
    const lastNextNode = nodes.filter(node => node.type === "next").slice(-1)[0];
    const newNode = {
      id: `node-${sessionNumber}-${nodes.length + 1}`,
      content: `Node ${nodes.length + 1}`,
      parentId: lastNextNode ? lastNextNode.id : null,
      type: "next",
    };
    setNodes([...nodes, newNode]);
  };

  const addFollowup = (parentId) => {
    const newFollowup = {
      id: `followup-${sessionNumber}-${nodes.length + 1}`,
      content: `Followup ${nodes.length + 1}`,
      parentId,
      type: "followup",
    };
    setNodes([...nodes, newFollowup]);
  };

  const removeNode = (id) => {
    setNodes(nodes.filter(node => node.id !== id && node.parentId !== id));
  };

  return (
    <div className="session-container">
      <h2>Theory Session {sessionNumber}</h2>
      <p>{content}</p>
      <button className="remove-btn" onClick={() => onRemove(sessionNumber)}>Remove</button>
      <button onClick={addNext}>Add Next</button>

      <div className="nodes-container">
        {nodes.map((node) =>
          node.type === "next" ? (
            <div className="next-node-container" key={node.id}>
              <NextNode
                id={node.id}
                content={node.content}
                parentId={node.parentId}
                addFollowup={addFollowup}
                onRemove={removeNode}
              />
              <div className="followup-container">
                {nodes
                  .filter(f => f.parentId === node.id && f.type === "followup")
                  .map(followup => (
                    <FollowupNode key={followup.id} id={followup.id} content={followup.content} parentId={followup.parentId} onRemove={removeNode} />
                  ))}
              </div>
            </div>
          ) : null
        )}
      </div>

      {nodes.map((node) =>
        node.parentId ? (
          <Xarrow key={node.id} start={node.parentId} end={node.id} />
        ) : null
      )}
    </div>
  );
};

export default TheorySession;
