import React from "react";

export default function Toolbar() {
  return (
    <div className="relative inset-x-0 top-0 z-10 flex items-center justify-betwe shadow-md p-4">
      <div className="flex-1 text-white">Home</div>
      <div className="flex-1 text-center text-white">Center Content</div>
      <div className="flex-1 text-right text-white">Right Side Content</div>
    </div>
  );
}
