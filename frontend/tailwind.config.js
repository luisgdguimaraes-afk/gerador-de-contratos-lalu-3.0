/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f4f6f2',
          100: '#e8ede4',
          200: '#b8c4a8',
          300: '#7a9a68',
          500: '#2f4521',
          600: '#2f4521',
          700: '#263a1b',
        },
        subtitle: '#c0a97c',
      },
    },
  },
  plugins: [],
}
