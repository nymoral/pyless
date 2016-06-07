from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch, Q
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from football.models import Game, Points, Guess

@login_required()
@require_http_methods(['GET'])
@cache_page(5 * 60)
@vary_on_cookie
def game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    guesses = Guess.objects.select_related('user__first_name', 'user__last_name').filter(
        game_id=game_id).order_by('points', 'user__first_name', 'user__last_name', 'id')

    ctx = {'game': game, 'guesses': guesses}
    return render(request, 'football/game.html', ctx)
