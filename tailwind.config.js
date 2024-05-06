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
      },
      spacing: {  // the lift-kit system https://youtu.be/9ElrcTtAxzA?si=qzYS4UmFXXpGPXm-&t=253
        'xs': '0.128em',
        'sm': '0.272em',
        'md': '0.618em',
        'lg': '1em',
        'xl': '1.618em',
        '2xl': '2.618em',
        'race-width': '45em',
      },
    },
  },
  plugins: [],
}

