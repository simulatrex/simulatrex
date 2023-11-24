import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/layouts/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#7ACAD5",
        accent: "#28383C",
        dark: "#17191C",
      },
      backgroundImage: {
        start: "url('/assets/start-bg.png')",
      },
    },
  },
  plugins: [],
};
export default config;
