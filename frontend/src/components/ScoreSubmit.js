import React, { useState } from 'react';
import { submitScore } from '../api/leaderboard';

const inputClass =
  'border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-decoGold bg-white text-decoNavy shadow-sm text-lg transition w-full placeholder-gray-400';
const labelClass =
  'block text-decoNavy font-semibold mb-2 ml-1';
const buttonClass =
  'bg-decoGold text-decoNavy px-6 py-3 rounded-lg font-bold hover:bg-yellow-400 transition border-2 border-decoGold shadow text-lg w-full flex items-center justify-center disabled:opacity-60 mt-2';

export default function ScoreSubmit() {
  const [userId, setUserId] = useState('');
  const [score, setScore] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setStatus('');
    setLoading(true);
    if (!userId || !score) {
      setError('Please enter both User ID and Score');
      setLoading(false);
      return;
    }
    const res = await submitScore(userId, score);
    setLoading(false);
    if (res.status === 'success') {
      setStatus('Score submitted successfully!');
      setUserId('');
      setScore('');
    } else {
      setError('Failed to submit score');
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-200 max-w-md mx-auto flex-1 flex flex-col items-center w-full mb-8">
      <h2 className="text-2xl font-bebas text-decoNavy mb-8 tracking-widest text-center">Submit Score</h2>
      <form className="flex flex-col gap-6 w-full" onSubmit={handleSubmit} autoComplete="off">
        <div className="flex flex-col gap-1">
          <label htmlFor="userId" className={labelClass}>User ID </label>
          <input
            id="userId"
            value={userId}
            onChange={e => setUserId(e.target.value)}
            placeholder="Enter User ID "
            className={inputClass + (error && !userId ? ' border-red-400' : '')}
            autoComplete="off"
          />
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="score" className={labelClass}>Score </label>
          <input
            id="score"
            value={score}
            onChange={e => setScore(e.target.value)}
            placeholder="Enter Score "
            type="number"
            className={inputClass + (error && !score ? ' border-red-400' : '')}
            autoComplete="off"
          />
        </div>
        <button
          type="submit"
          className={buttonClass}
          disabled={loading}
        >
          {loading && (
            <svg className="animate-spin h-5 w-5 mr-2 text-decoNavy" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
            </svg>
          )}
          Submit
        </button>
        {error && <div className="text-red-500 text-center text-sm -mt-2">{error}</div>}
        {status && <div className="text-green-500 font-semibold text-center text-sm -mt-2">{status}</div>}
      </form>
    </div>
  );
}
