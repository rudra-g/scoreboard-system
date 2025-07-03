from celery import shared_task
from django.db import transaction, connection
from leaderboard.cache import redis_client, cache_delete
from leaderboard.models import GameSession, Leaderboard
from django.db.models import Sum
from contextlib import contextmanager
import time

@contextmanager
def redis_mutex(key, timeout=60, retry_interval=0.5, max_wait=60):
    lock = redis_client.lock(key, timeout=timeout)
    start = time.time()
    while True:
        acquired = lock.acquire(blocking=False)
        if acquired:
            try:
                yield
            finally:
                lock.release()
            return
        elif time.time() - start > max_wait:
            raise TimeoutError(f"Could not acquire Redis lock on {key} within {max_wait} seconds")
        time.sleep(retry_interval)
        
        
def delete_all_user_rank_caches():
    # Use the Redis SCAN command for safe iteration (avoids blocking Redis)
    cursor = 0
    pattern = "leaderboard:rank:*"
    while True:
        cursor, keys = redis_client.scan(cursor=cursor, match=pattern, count=1000)
        if keys:
            redis_client.delete(*keys)
        if cursor == 0:
            break


def recalculate_leaderboard():
    with redis_mutex("leaderboard:mutex", timeout=60):
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM leaderboard_leaderboard;")
                cursor.execute("""
                    INSERT INTO leaderboard_leaderboard (user_id, total_score, rank)
                    SELECT
                        gs.user_id,
                        SUM(gs.score) AS total_score,
                        RANK() OVER (ORDER BY SUM(gs.score) DESC) AS rank
                    FROM leaderboard_gamesession gs
                    GROUP BY gs.user_id;
                """)
                cache_delete('leaderboard:top10')
                delete_all_user_rank_caches()

@shared_task
def update_leaderboard_ranks():
    if redis_client.get('leaderboard:dirty'):
        print("Going in to recalculate rank")
        redis_client.delete('leaderboard:dirty') 
        recalculate_leaderboard()
        