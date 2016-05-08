from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from enum import Enum


class Team(models.Model):
    """Team is one side of a match.
    Teams are identified by their country code (which serves as primary key).
    """

    short = models.CharField(max_length=8, primary_key=True)
    full_name = models.CharField(max_length=32)

    def __str__(self):
        return '{name}'.format(name=self.short)


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

    @property
    def mark(self):
        """A helper property to get stage of a game"""
        if self.ended != None:
            return 'E({r1} - {r2})'.format(r1=self.result1, r2=self.result2)
        if self.closed != None:
            return 'C({time:%H:%M})'.format(time=self.closed)
        return 'O'

    def __str__(self):
        return '{t1} - {t2} {time:%Y-%m-%d %H:%M} [{status}]'.format(t1=self.team1, t2=self.team2, time=self.time, status=self.mark)

    def clean(self):
        """Ensure correct state of a game.
        Close a game if it is ending.
        Throw error if game that is ending does not have a valid result.
        """

        if self.ended != None and (self.result1 == None or self.result2 == None):
            raise ValidationError('Game that has ended must have result set')
        if self.ended != None and self.closed == None:
            self.closed = self.ended


class Guess(models.Model):
    """A guess is prediction that user makes on the outcome of a game."""
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='+')
    result1 = models.IntegerField()
    relust2 = models.IntegerField()
    subbmited = models.DateTimeField(auto_now_add=True)


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
    """Here points will be calculated"""
    pass


@receiver(post_save, sender=User)
def after_user_save(sender, instance, **kwargs):
    """Create a points object for a user"""
    try:
        instance.points
    except ObjectDoesNotExist:
        p = Points(user=instance)
        p.save()
