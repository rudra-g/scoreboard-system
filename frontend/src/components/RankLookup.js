import React, { useState } from 'react';
import { fetchUserRank } from '../api/leaderboard';

export default function RankLookup() {
  const [userId, setUserId] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleLookup = async () => {
    setError('');
    setResult(null);
    if (!userId) {
      setError('Please enter a User ID');
      return;
    }
    const res = await fetchUserRank(userId);
    if (res.error) {
      setError('User not found');
    } else {
      setResult(res);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-200 max-w-md mx-auto flex-1 flex flex-col items-center">
      <h2 className="text-2xl font-bebas text-decoNavy mb-6 tracking-widest text-center">Lookup User Rank</h2>
      <div className="flex flex-col sm:flex-row items-center gap-3 mb-4 w-full justify-center">
        <input
          value={userId}
          onChange={e => setUserId(e.target.value)}
          placeholder="User ID "
          className="border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-decoGold w-full sm:w-40 bg-white text-decoNavy shadow-sm text-lg transition"
        />
        <button
          onClick={handleLookup}
          className="bg-decoGold text-decoNavy px-6 py-3 rounded-lg font-bold hover:bg-yellow-400 transition border-2 border-decoGold shadow text-lg w-full sm:w-auto"
        >
          Lookup
        </button>
      </div>
      {error && <div className="text-red-500 mb-2 text-center">{error}</div>}
      {result && (
        <div className="bg-gray-50 rounded-lg p-4 text-decoNavy border border-decoGold mt-2 text-center w-full">
          <div className="font-semibold">Rank: <span className="text-lg font-bebas">{result.rank}</span></div>
          <div>Total Score: <span className="font-mono">{result.total_score}</span></div>
        </div>
      )}
    </div>
  );
}
