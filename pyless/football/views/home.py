from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from football.models import Points
from django.db.models import Avg


@login_required()
@require_http_methods(['GET'])
def home(request):
    points = Points.objects.select_related(
        'user__first_name', 'user__last_name').order_by('points', 'user_id').filter(user__is_active=True)
    aggregate = Points.objects.aggregate(Avg('points'), Avg('correct'))
    return render(request, 'football/home.html', {'points': points, 'aggregate': aggregate})
