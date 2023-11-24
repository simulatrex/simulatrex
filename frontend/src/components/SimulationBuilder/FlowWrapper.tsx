import React, { useCallback } from "react";
import ReactFlow, {
  Edge,
  MarkerType,
  Node,
  MiniMap,
  Controls,
  addEdge,
  useEdgesState,
  useNodesState,
  Background,
} from "reactflow";
import CustomNode from "./CustomNode";

import "reactflow/dist/style.css";
import { logger } from "@/utils/logger";

export const initialNodes: Node[] = [
  {
    id: "1",
    type: "input",
    data: {
      label: "Target group",
    },
    position: { x: 250, y: 0 },
  },
  {
    id: "2",
    data: {
      label: "Target group",
    },
    position: { x: 100, y: 100 },
  },
  {
    id: "3",
    type: "output",
    data: {
      label: "Target group",
    },
    position: { x: 400, y: 100 },
  },
];

export const initialEdges: Edge[] = [
  { id: "e1-2", source: "1", target: "2", animated: true },
  { id: "e1-3", source: "1", target: "3", animated: true },
  {
    id: "e4-5",
    source: "4",
    target: "5",
    type: "smoothstep",
    sourceHandle: "handle-0",
    data: {
      selectIndex: 0,
    },
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
  {
    id: "e4-6",
    source: "4",
    target: "6",
    type: "smoothstep",
    sourceHandle: "handle-1",
    data: {
      selectIndex: 1,
    },
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
];

const nodeTypes = {
  custom: CustomNode,
};

const minimapStyle = {
  height: 120,
};

const onInit = (reactFlowInstance: any) =>
  logger.debug("flow loaded:", reactFlowInstance);

const FlowWrapper = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const onConnect = useCallback(
    (params: any) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  // we are using a bit of a shortcut here to adjust the edge type
  // this could also be done with a custom edge for example
  const edgesWithUpdatedTypes = edges.map((edge) => {
    if (edge.sourceHandle) {
      const edgeType = nodes.find((node) => node.type === "custom")?.data
        .selects[edge.sourceHandle];
      edge.type = edgeType;
    }

    return edge;
  });

  return (
    <div className="w-full h-[90vh]">
      <ReactFlow
        nodes={nodes}
        edges={edgesWithUpdatedTypes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onInit={onInit}
        fitView
        nodeTypes={nodeTypes}
      >
        <MiniMap style={minimapStyle} zoomable pannable />
        <Controls />
        <Background color="#aaa" gap={16} />
      </ReactFlow>
    </div>
  );
};

export default FlowWrapper;
