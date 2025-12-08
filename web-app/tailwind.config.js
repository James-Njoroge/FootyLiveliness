/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'pl-purple': '#3d195b',
        'pl-pink': '#e90052',
      },
    },
  },
  plugins: [],
}
