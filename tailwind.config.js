/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'text-color': '#9EC8B9',
        'background-color': '#092635',
        'primary-color': '#1B4242',
        'secondary-color': '#5C8374',
        'accent-color': '#EC4899',
        'hover-accent-color': '#F01883',
        'ignore-color': '#919191',
      }  
    }
  },
  plugins: [],
}

