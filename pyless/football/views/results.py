
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.db.models import Q

from football.models import Points, Game, Guess

@login_required()
@require_http_methods(['GET'])
@cache_page(5 * 60)
@vary_on_cookie
def results_view(request):
    return render(request, 'football/results.html', {'data': make_results_data()})


@login_required()
@require_http_methods(['GET'])
@cache_page(5 * 60)
@vary_on_cookie
def results_small_view(request):
    return render(request, 'football/results.html', {'data':  make_results_data(4), 'small': True})


def make_results_data(limit=None):
    with transaction.atomic():
        games = Game.objects.select_related('team1', 'team2').exclude(closed=None)
        if not limit:
            games = games.order_by('time', 'id')
        else:
            # Reversed ordering to get last `limit` items.
            games = games.order_by('-time', '-id')[:limit]
        guesses = Guess.objects.all()
        points = Points.objects.select_related('user__first_name', 'user__last_name').order_by(
            'points', '-correct', 'user_id').filter(user__is_active=True)
        if limit:
            games = games[::-1]
        d = list({'points': p, 'guesses': extract_guesses(
            prepare_guesses(guesses), games, p)} for p in points)
        return {'games': list(games), 'points': list(points), 'guesses': d}


def prepare_guesses(guesses):
    r = {}
    for g in guesses:
        if g.user_id not in r:
            r[g.user_id] = {g.game_id: g}
        else:
            r[g.user_id][g.game_id] = g
    return r


def extract_guesses(guesses, games, p):
    guesses = guesses.get(p.user_id)
    if guesses is None:
        return None
    return list(guesses.get(game.id) for game in games)

