from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Prefetch, Q
from django.http.response import JsonResponse, HttpResponseForbidden, HttpResponseGone

from football.models import Game, Points, Guess

import re


@login_required()
@require_http_methods(['GET', 'POST'])
def guesses_view(request, user_id):
    """Guesses view
    It always displays the guesses table (with success message on POST)."""

    user_id = int(user_id)

    ctx = {'own': user_id == request.user.id}
    if request.method == 'POST':
        submit(request, ctx)

    games = Game.objects.prefetch_related(Prefetch('guesses', queryset=Guess.objects.filter(
        user_id=user_id), to_attr='users_guess')).select_related('team1', 'team2').order_by('time')
    points = Points.objects.get(user_id=user_id)
    ctx.update({'selected_id': user_id, 'games': games,
                'points': points})
    return render(request, 'football/guesses.html', ctx)

@login_required()
@require_http_methods(['PUT'])
def guess_ajax(request, user_id, game_id, g1, g2):
    user_id = int(user_id)
    game_id = int(game_id)
    g1 = int(g1)
    g2 = int(g2)
    if user_id != request.user.id:
        return HttpResponseForbidden()
    game = Game.objects.filter(closed=None, id=game_id)[:1]
    if len(game) == 0:
        return HttpResponseGone()

    result = update_single_guess(user_id, game_id, tuple((g1, g2)))
    return JsonResponse({'created': result[1]})


def submit(request, ctx):
    form = request.POST
    games = Game.objects.filter(closed=None)
    updated = False
    for game in games:
        guess = extract_guess(form.get(game.input_name))
        if guess:
            update_single_guess(request.user.id, game.id, guess)
            updated = True
    ctx['updated'] = updated

def update_single_guess(user_id, game_id, guess):
    return Guess.objects.update_or_create(user_id=user_id, game_id=game_id,
        defaults={'result1': guess[0], 'result2': guess[1]})

guess_re = re.compile(r'^.*(\d+).*([-_:;., ]).*(\d+).*$')


def extract_guess(s):
    if s is None:
        return None
    m = guess_re.match(s)
    if not m:
        return None
    return tuple(int(x) for x in m.group(1, 3))
