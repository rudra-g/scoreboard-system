export async function fetchTopLeaderboard() {
  const res = await fetch('/api/leaderboard/top');
  return res.json();
}

export async function fetchUserRank(userId) {
  const res = await fetch(`/api/leaderboard/rank/${userId}`);
  return res.json();
}

export async function submitScore(userId, score) {
  const res = await fetch('/api/leaderboard/submit', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({user_id: userId, score}),
  });
  return res.json();
}
