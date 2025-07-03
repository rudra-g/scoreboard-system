from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.db import transaction, connection
from .models import User, GameSession, Leaderboard
from .cache import cache_get, cache_set, cache_delete
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.db.models import Sum
from leaderboard.cache import redis_client
from .tasks import redis_mutex

@method_decorator(csrf_exempt, name='dispatch')
class SubmitScoreView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = int(data['user_id'])
            score = int(data['score'])
            game_mode = data.get('game_mode', 'solo')
        except (KeyError, ValueError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid input")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponseNotFound("User does not exist")

        with transaction.atomic():
            GameSession.objects.create(user=user, score=score, game_mode=game_mode)
            redis_client.set('leaderboard:dirty', 1)
            cache_delete(f'leaderboard:rank:{user_id}')

        return JsonResponse({'status': 'success'})


class TopLeaderboardView(View):
    def get(self, request):
        cache_key = 'leaderboard:top10'
        cached = cache_get(cache_key)
        if cached:
            return JsonResponse({'leaderboard': json.loads(cached)})
        top_entries = Leaderboard.objects.select_related('user').order_by('rank')[:10]
        leaderboard = [
            {'user_id': entry.user.id, 'username': entry.user.username, 'total_score': entry.total_score, 'rank': entry.rank}
            for entry in top_entries
        ]
        cache_set(cache_key, json.dumps(leaderboard))
        return JsonResponse({'leaderboard': leaderboard})
    
    

class UserRankView(View):
    def get(self, request, user_id):
        cache_key = f'leaderboard:rank:{user_id}'
        cached = cache_get(cache_key)
        if cached:
            return JsonResponse(json.loads(cached))
        try:
            entry = Leaderboard.objects.select_related('user').get(user__id=user_id)
            result = {
                'user_id': entry.user.id,
                'username': entry.user.username,
                'total_score': entry.total_score,
                'rank': entry.rank
            }
        except Leaderboard.DoesNotExist:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            total_score = GameSession.objects.filter(user=user).aggregate(Sum('score'))['score__sum'] or 0
            result = {
                'user_id': user.id,
                'username': user.username,
                'total_score': total_score,
                'rank': 0  # not in the leaderboard yet
            }

        cache_set(cache_key, json.dumps(result))
        return JsonResponse(result)