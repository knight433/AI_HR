import React from "react";
import Xarrow from "react-xarrows";

const FollowupNode = ({ id, content, parentId, onRemove }) => {
  return (
    <div className="node followup-node" id={id}>
      <button className="close-btn" onClick={() => onRemove(id)}>✖</button>
      <p>{content}</p>

      {parentId && <Xarrow start={parentId} end={id} />}
    </div>
  );
};

export default FollowupNode;
