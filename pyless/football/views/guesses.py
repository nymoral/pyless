from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Prefetch, Q

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


def submit(request, ctx):
    form = request.POST
    games = Game.objects.filter(closed=None)
    updated = False
    for game in games:
        guess = extract_guess(form.get(game.input_name))
        if guess:
            Guess.objects.update_or_create(
                user=request.user, game_id=game.id, defaults={'result1': guess[0], 'result2': guess[1]})
            updated = True
    ctx['updated'] = updated

guess_re = re.compile(r'^.*(\d+).*([-_:;., ]).*(\d+).*$')


def extract_guess(s):
    if s is None:
        return None
    m = guess_re.match(s)
    if not m:
        return None
    return tuple(int(x) for x in m.group(1, 3))
