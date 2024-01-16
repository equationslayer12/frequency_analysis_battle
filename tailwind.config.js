/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'primary-color': '#092635',
        'secondary-color': '#1B4242',
        'third-color': '5C8374',
        'accent-color': '#9EC8B9',
        'ignore-color': '#919191',
      }  
    }
  },
  plugins: [],
}

