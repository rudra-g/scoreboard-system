from django.urls import path
from .views import SubmitScoreView, TopLeaderboardView, UserRankView

urlpatterns = [
    path('api/leaderboard/submit', SubmitScoreView.as_view()),
    path('api/leaderboard/top', TopLeaderboardView.as_view()),
    path('api/leaderboard/rank/<int:user_id>', UserRankView.as_view()),
]
