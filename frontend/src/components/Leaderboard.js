import React, { useEffect, useState } from 'react';
import { fetchTopLeaderboard } from '../api/leaderboard';

const rankColors = [
  'bg-yellow-200 text-yellow-900 font-bold', // 1st
  'bg-gray-200 text-gray-900 font-bold',    // 2nd
  'bg-emerald-200 text-emerald-900 font-bold', // 3rd
];

export default function Leaderboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const poll = () => {
      fetchTopLeaderboard().then(res => setData(res.leaderboard));
    };
    poll();
    const interval = setInterval(poll, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 mb-10 border border-gray-200">
      <h2 className="text-3xl font-bebas text-decoNavy mb-6 tracking-widest text-center">Top 10 Leaderboard</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 font-montserrat">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-bold text-decoNavy uppercase tracking-wider">Rank</th>
              <th className="px-6 py-3 text-left text-xs font-bold text-decoNavy uppercase tracking-wider">Username</th>
              <th className="px-6 py-3 text-left text-xs font-bold text-decoNavy uppercase tracking-wider">Total Score</th>
            </tr>
          </thead>
          <tbody>
            {data.map((user, idx) => (
              <tr key={user.user_id} className={idx < 3 ? rankColors[idx] : idx % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                <td className="px-6 py-3 text-lg">#{idx + 1}</td>
                <td className="px-6 py-3">{user.username}</td>
                <td className="px-6 py-3">{user.total_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
