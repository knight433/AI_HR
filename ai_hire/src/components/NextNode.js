import React from "react";
import Xarrow from "react-xarrows";

const NextNode = ({ id, content, parentId, addFollowup, onRemove }) => {
  return (
    <div className="node next-node" id={id}>
      <button className="close-btn" onClick={() => onRemove(id)}>✖</button>
      <p>{content}</p>
      <button onClick={() => addFollowup(id)}>Add Followup</button>

      {parentId && <Xarrow start={parentId} end={id} />}
    </div>
  );
};

export default NextNode;
