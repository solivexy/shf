import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#131722",
        surface: "#1e222d",
        surfaceHover: "#2a2e39",
        borderDark: "#2a2e39",
        textPrimary: "#d1d4dc",
        textSecondary: "#787b86",
        accent: "#2962ff",
        success: "#089981",
        warning: "#f2a900",
        danger: "#f23645",
      },
    },
  },
  plugins: [],
};
export default config;
