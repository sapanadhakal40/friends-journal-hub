/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/templates/**/*.html', // Adjust this path based on where your HTML files are located
    './app/static/js/**/*.js'     // If you have JavaScript files in a static folder
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

