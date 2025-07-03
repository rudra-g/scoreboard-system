import random
import time
import requests
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Sum
from leaderboard.models import User, GameSession, Leaderboard

API_BASE_URL = "http://localhost:8000/api/leaderboard"
BATCH_SIZE = 10000


class Command(BaseCommand):
    help = "Populate DB and/or simulate leaderboard API interactions"

    def add_arguments(self, parser):
        parser.add_argument(
            '--populate', action='store_true', help='Populate database with initial data'
        )
        parser.add_argument(
            '--simulate', action='store_true', help='Start simulation of API calls (runs indefinitely)'
        )

    def handle(self, *args, **options):
        if options['populate']:
            self.populate_database()
        if options['simulate']:
            self.simulate_api_calls()

    def populate_database(self):
        self.stdout.write("Deleting old data...")
        User.objects.all().delete()
        GameSession.objects.all().delete()
        Leaderboard.objects.all().delete()

        self.stdout.write("Creating users...")
        users = []
        for i in range(1, 1_000_001):
            users.append(User(username=f"user_{i}"))
            if i % BATCH_SIZE == 0:
                User.objects.bulk_create(users)
                users = []
                self.stdout.write(f"Inserted {i} users")
        if users:
            User.objects.bulk_create(users)
        self.stdout.write("Users created.")

        self.stdout.write("Creating game sessions...")
        user_ids = list(User.objects.values_list('id', flat=True))
        sessions = []
        for i in range(1, 5_000_001):
            sessions.append(GameSession(
                user_id=random.choice(user_ids),
                score=random.randint(1, 10000),
                game_mode='solo' if random.random() > 0.5 else 'team',
                timestamp=timezone.now() - timedelta(days=random.randint(0, 364))
            ))
            if i % BATCH_SIZE == 0:
                GameSession.objects.bulk_create(sessions)
                sessions = []
                self.stdout.write(f"Inserted {i} game sessions")
        if sessions:
            GameSession.objects.bulk_create(sessions)
        self.stdout.write("Game sessions created.")

        self.stdout.write("Creating leaderboard...")
        scores = User.objects.annotate(total_score=Sum('sessions__score')).order_by('-total_score')
        rank = 1
        leaderboard_rows = []
        for user in scores:
            if user.total_score is None:
                continue
            leaderboard_rows.append(Leaderboard(
                user_id=user.id,
                total_score=user.total_score,
                rank=rank
            ))
            rank += 1

        for i in range(0, len(leaderboard_rows), BATCH_SIZE):
            Leaderboard.objects.bulk_create(leaderboard_rows[i:i + BATCH_SIZE])
            self.stdout.write(f"Inserted {i + BATCH_SIZE} leaderboard entries")
        self.stdout.write("Leaderboard created.")

    def simulate_api_calls(self):
        self.stdout.write("Starting API simulation (press Ctrl+C to stop)...")
        try:
            while True:
                user_id = random.randint(1, 1_000_000)
                self.submit_score(user_id)
                top_players = self.get_top_players()
                user_rank = self.get_user_rank(user_id)
                self.stdout.write(f"Submitted score for user {user_id}")
                self.stdout.write(f"Top players: {top_players}")
                self.stdout.write(f"Rank for user {user_id}: {user_rank}")
                time.sleep(random.uniform(0.5, 2))
        except KeyboardInterrupt:
            self.stdout.write("Simulation stopped by user.")

    def submit_score(self, user_id):
        score = random.randint(100, 10000)
        try:
            requests.post(f"{API_BASE_URL}/submit", json={"user_id": user_id, "score": score})
        except requests.RequestException as e:
            self.stdout.write(f"Failed to submit score for user {user_id}: {e}")

    def get_top_players(self):
        try:
            response = requests.get(f"{API_BASE_URL}/top")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.stdout.write(f"Failed to fetch top players: {e}")
            return {}

    def get_user_rank(self, user_id):
        try:
            response = requests.get(f"{API_BASE_URL}/rank/{user_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.stdout.write(f"Failed to fetch rank for user {user_id}: {e}")
            return {}
