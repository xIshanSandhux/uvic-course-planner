/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#F4D06F",     // Yellow
        accent: "#FF8811",      // Orange
        cyan: "#9DD9D2",        // Cyan
        offwhite: "#FFF8F0",    // Soft off-white background
        purple: "#392F5A",       // Deep purple 
        dark: "#1a1a1a",        // Optional: dark text or base bg
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        xl: '1rem',
        '2xl': '1.5rem',
      },
      boxShadow: {
        soft: '0 4px 12px rgba(0, 0, 0, 0.4)',
        strong: '0 6px 20px rgba(0, 0, 0, 0.2)',
      },
    },
  },
  plugins: [],
}
