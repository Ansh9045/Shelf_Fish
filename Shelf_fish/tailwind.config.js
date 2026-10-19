/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}",
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors:{
        'deep-red' : '#7a0000',
        'gold' : '#f8ea28',
        'panel' : '#ece58d',
        'dark-gray' : '#141414'
      }
    },
  },
  plugins: [],
};