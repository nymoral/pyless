from django.core.management.base import BaseCommand, CommandError
from football.models import Game
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Closes games that will soon start.'


    def handle(self, *args, **options):
        c = 0
        for g in Game.objects.filter(time__lte=timezone.now()+timedelta(minutes=5), closed=None):
            g.closed = timezone.now()
            g.save()
            self.stdout.write('Game closed: {}'.format(g))
            c += 1
        if c > 0:
            self.stdout.write('{} games closed'.format(c))
