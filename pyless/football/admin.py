from django.contrib import admin

from .models import Team, Game, Guess, Points


admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Guess)
admin.site.register(Points)
