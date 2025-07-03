import React from 'react';
import Leaderboard from './components/Leaderboard';
import RankLookup from './components/RankLookup';
import ScoreSubmit from './components/ScoreSubmit';

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-full bg-transparent">
      <div className="w-full max-w-4xl px-4">
        <header className="mb-8 text-center">
          <h1 className="text-5xl font-extrabold text-decoNavy mb-2 font-bebas">Sports Score Leaderboard</h1>
          <div className="flex justify-center mb-4">
            <span className="block w-24 h-1 bg-gradient-to-r from-decoGold via-yellow-400 to-decoGold rounded-full"></span>
          </div>
          <p className="text-lg text-decoNavy tracking-widest uppercase font-montserrat">Live, scalable, and beautiful leaderboard system</p>
        </header>
        <Leaderboard />
        <div className="flex flex-col md:flex-row gap-8 justify-center items-center">
          <RankLookup />
          <ScoreSubmit />
        </div>
      </div>
    </div>
  );
}

export default App;
