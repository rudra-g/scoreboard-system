from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class GameSession(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    score = models.IntegerField()
    game_mode = models.CharField(max_length=50, default='solo')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['-score']),
        ]

class Leaderboard(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    total_score = models.IntegerField()
    rank = models.IntegerField()
