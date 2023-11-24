import React from "react";

import Toolbar from "@/components/SimulationBuilder/Toolbar";
import FlowWrapper from "@/components/SimulationBuilder/FlowWrapper";
import Panel from "@/components/SimulationBuilder/Panel";

type SimulationBuilderLayoutProps = {
  children: React.ReactNode;
};

export default function SimulationBuilderLayout({
  children,
}: SimulationBuilderLayoutProps) {
  return (
    <div className="flex flex-col">
      <div className="">
        <Toolbar />
      </div>
      <div className="content">
        <FlowWrapper />
      </div>
      <div className="">
        <Panel />
      </div>
    </div>
  );
}
