from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, When, Sum
from django.core.cache import cache

import uuid

from enum import Enum


class Team(models.Model):
    """Team is one side of a match.
    Teams are identified by their country code (which serves as primary key).
    """

    short = models.CharField(max_length=8, primary_key=True)
    full_name = models.CharField(max_length=32)

    class Meta:
        ordering = ['full_name']



    def __str__(self):
        return '{name}'.format(name=self.full_name)


class Game(models.Model):
    """A game is a match between two teams.
    A game can be in three stages:
        * Open (users can still guess on its outcome).
        * Closed (users cannot make guesses but can see other peoples guesses on this game).
        * Ended (game that has ended). After a game has ended points are calculated.
    """

    team1 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='+')
    team2 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='+')
    time = models.DateTimeField()
    closed = models.DateTimeField(blank=True, default=None, null=True)
    ended = models.DateTimeField(blank=True, default=None, null=True)
    result1 = models.IntegerField(blank=True, null=True)
    result2 = models.IntegerField(blank=True, null=True)
    important = models.BooleanField(default=False)

    @property
    def mark(self):
        """A helper property to get stage of a game"""
        if self.ended != None:
            return 'E({})'.format(self.result)
        if self.closed != None:
            return 'C({time:%H:%M})'.format(time=self.closed)
        return 'O'

    def __str__(self):
        return '{t1} - {t2} {time:%Y-%m-%d %H:%M} [{status}]'.format(t1=self.team1_id, t2=self.team2_id, time=self.time, status=self.mark)

    def clean(self):
        """Ensure correct state of a game.
        Close a game if it is ending.
        Throw error if game that is ending does not have a valid result.
        """

        if self.ended != None and (self.result1 == None or self.result2 == None):
            raise ValidationError('Game that has ended must have result set')
        if self.ended != None and self.closed == None:
            self.closed = self.ended

    @property
    def result(self):
        if self.ended is None:
            return '-'
        else:
            return '{} : {}'.format(self.result1, self.result2)

    @property
    def input_name(self):
        return 'game_input_{}'.format(self.id)

    @property
    def short_teams(self):
        return '{} - {}'.format(self.team1.short, self.team2.short)

    @property
    def long_teams(self):
        return '{} - {}'.format(self.team1.full_name, self.team2.full_name)


class Guess(models.Model):
    """A guess is prediction that user makes on the outcome of a game."""
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='guesses')
    game = models.ForeignKey(
        Game, on_delete=models.PROTECT, related_name='guesses')
    result1 = models.IntegerField(blank=True, null=True)
    result2 = models.IntegerField(blank=True, null=True)
    subbmited = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return 'G({}) U({})  {}'.format(self.game.id, self.user.id, self.result)

    @property
    def result(self):
        if self.late:
            return '-'
        return '{} : {}'.format(self.result1, self.result2)

    @property
    def correct(self):
        return self.points != None and self.points < 0

    @property
    def late(self):
        return self.result1 is None or self.result2 is None

    @property
    def form_points(self):
        if self.points != None:
            return self.points
        else:
            return '-'

    def calc(self, res, penalty=None, only=False):
        corr_out = False
        if penalty and self.late:
            self.points = penalty
        elif res == (self.result1, self.result2):
            self.points = -7 if only else -3
            corr_out = True
        else:
            self.points = 0
            corr_out = game_outcome(self.result1, self.result2) == game_outcome(*res)
            if not corr_out:
                self.points += 3
            self.points += sum(abs(a-b) for a, b in zip((self.result1, self.result2), res))
        return self.points, corr_out


class Points(models.Model):
    """Points is single users results used to sort and display results table"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    points = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=Game)
def after_game_save(sender, instance, **kwargs):
    """Create missing guesses and calculate points"""
    if instance.closed:
        game_closed(instance)
    if instance.ended:
        game_ended(instance)
    cache.clear()


@receiver(post_save, sender=User)
def after_user_save(sender, instance, **kwargs):
    """Create a points object for a user
    Fill guesses of games a user has missed"""
    try:
        instance.points
    except ObjectDoesNotExist:
        p = Points(user=instance)
        p.save()
    for game in Game.objects.exclude(closed=None).only('id'):
        game_closed(game, instance.id)


def game_closed(game, user_id=None):
    """Insert empty guess for user (each user if user_id is None) that didn't submit a guess"""
    users = User.objects.exclude(guesses__game_id=game.id)
    if user_id:
        users = users.filter(id=user_id)
    guesses = [Guess(user_id=user.id, game_id=game.id)
               for user in users.only('id')]
    Guess.objects.bulk_create(guesses)


def game_outcome(r1, r2):
    """Returns 1 if first team won, 2 if second and 0 if it was a draw"""
    if r1 > r2: return 1
    if r2 > r1: return 2
    return 0


def game_ended(game):
    """Recalculate points in this game guesses and update the total in points model"""
    res = (game.result1, game.result2)
    guesses = Guess.objects.filter(game_id=game.id).all()
    points = list(map(lambda g: g.calc(res), guesses))
    penalty = max(p(0) for p in points) if len(points) > 0 else None
    only = sum(1 for p in points if p(1)) == 1
    for g in guesses:
        g.calc(res, penalty, only)
        g.save()

    for p in Points.objects.annotate(total_points=Sum('user__guesses__points'), total_correct=Sum(Case(When(user__guesses__points__lte=-3, then=1), default=0, output_field=models.IntegerField()))):
        p.points = p.total_points
        p.correct = p.total_correct
        p.save()


class Reminder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    