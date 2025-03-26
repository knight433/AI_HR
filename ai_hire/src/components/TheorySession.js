import React, { useState, useEffect } from "react";
import NextNode from "./NextNode";
import FollowupNode from "./FollowupNode";
import Xarrow, { useXarrow } from "react-xarrows";

const TheorySession = ({ sessionNumber, content, onRemove, getSessionData }) => {
  const [nodes, setNodes] = useState([]);
  const updateXarrow = useXarrow();

  useEffect(() => {
    updateXarrow();
    getSessionData(sessionNumber, { sessionNumber, nodes });
  }, [nodes, sessionNumber, getSessionData, updateXarrow]);

  const addNext = () => {
    const lastNextNode = nodes.filter(node => node.type === "next").slice(-1)[0];
    const newNode = {
      id: `node-${sessionNumber}-${nodes.length + 1}`,
      content: `Node ${nodes.length + 1}`,
      parentId: lastNextNode ? lastNextNode.id : null,
      type: "next",
      skill: "",
      question: "",
      level: 1,
    };
    setNodes([...nodes, newNode]);
  };

  const addFollowup = (parentId) => {
    const newFollowup = {
      id: `followup-${sessionNumber}-${nodes.length + 1}`,
      content: `Followup ${nodes.length + 1}`,
      parentId,
      type: "followup",
      follow_up: "",
    };
    setNodes([...nodes, newFollowup]);
  };

  const updateNodeData = (id, skill, question, level) => {
    setNodes(prevNodes => prevNodes.map(node => 
      node.id === id ? { ...node, skill, question, level } : node
    ));
  };

  const updateFollowupData = (id, question) => {
    setNodes(prevNodes => prevNodes.map(node => 
      node.id === id ? { ...node, follow_up: question } : node
    ));
  };

  const removeNode = (id) => {
    setNodes(nodes.filter(node => node.id !== id && node.parentId !== id));
  };

  return (
    <div className="session-container">
      <button className="remove-btn" onClick={() => onRemove(sessionNumber)}>Remove</button>
      <h2>Theory Session {sessionNumber}</h2>
      <p>{content}</p>
      <button className="add-next-btn" onClick={addNext}>Add Next</button>

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
                updateNodeData={updateNodeData}
              />
              <div className="followup-container">
                {nodes
                  .filter(f => f.parentId === node.id && f.type === "followup")
                  .map(followup => (
                    <FollowupNode 
                      key={followup.id} 
                      id={followup.id} 
                      content={followup.content} 
                      parentId={followup.parentId} 
                      onRemove={removeNode} 
                      updateNodeData={updateFollowupData}
                    />
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
