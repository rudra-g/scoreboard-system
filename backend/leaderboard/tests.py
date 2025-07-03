from django.test import TestCase, Client
from .models import User, GameSession
from .cache import cache_set, cache_get, cache_delete

class LeaderboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        GameSession.objects.create(user=self.user, score=100)
        self.client = Client()

    def test_submit_score(self):
        response = self.client.post('/api/leaderboard/submit', data={'user_id': self.user.id, 'score': 50}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_top_leaderboard(self):
        response = self.client.get('/api/leaderboard/top')
        self.assertEqual(response.status_code, 200)
        self.assertIn('leaderboard', response.json())

    def test_user_rank(self):
        response = self.client.get(f'/api/leaderboard/rank/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('rank', response.json())

    def test_cache_helpers(self):
        cache_set('testkey', 'testvalue', ttl=1)
        self.assertEqual(cache_get('testkey'), 'testvalue')
        cache_delete('testkey')
        self.assertIsNone(cache_get('testkey'))
