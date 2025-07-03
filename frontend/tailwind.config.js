module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
    './public/index.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        montserrat: ['Montserrat', 'sans-serif'],
        bebas: ['Bebas Neue', 'cursive'],
      },
      colors: {
        decoGold: '#FFD700',
        decoNavy: '#181c23',
        decoEmerald: '#50C878',
        decoSilver: '#C0C0C0',
        decoBronze: '#CD7F32',
      },
    },
  },
  plugins: [],
}; 