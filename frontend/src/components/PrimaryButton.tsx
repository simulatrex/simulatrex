import React from "react";

import Link from "next/link";

type PrimaryButtonProps = {
  children: React.ReactNode;
  href?: string;
  target?: string;
  onClick?: () => void;
};

const PrimaryButton: React.FC<PrimaryButtonProps> = ({
  children,
  href,
  target,
  onClick,
}) => {
  if (href) {
    return (
      <Link
        className="w-auto flex justify-center px-4 py-3 font-bold text-primary bg-white rounded-full hover:opacity-75 max-w-sm"
        href={href}
        target={target}
      >
        {children}
      </Link>
    );
  }

  return (
    <button
      className="w-auto px-4 py-3 font-bold text-primary bg-white rounded-full hover:opacity-75 max-w-sm"
      onClick={onClick}
    >
      {children}
    </button>
  );
};

export default PrimaryButton;
