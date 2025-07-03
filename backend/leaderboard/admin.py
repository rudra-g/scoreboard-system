from django.contrib import admin
from .models import User, GameSession, Leaderboard

admin.site.register(User)
admin.site.register(GameSession)
admin.site.register(Leaderboard)
