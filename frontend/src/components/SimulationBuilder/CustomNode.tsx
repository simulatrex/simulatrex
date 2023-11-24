import React, { memo } from "react";
import { Handle, useReactFlow, useStoreApi, Position } from "reactflow";

type CustomNodeProps = {
  id: string;
  data: {
    selects: {
      [key: string]: string;
    };
  };
};

function CustomNode({ id, data }: CustomNodeProps) {
  return (
    <>
      <div className="custom-node__header">
        This is a <strong>custom node</strong>
      </div>
    </>
  );
}

export default memo(CustomNode);
