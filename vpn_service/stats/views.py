from django.shortcuts import render
from stats.models import UserActivity
from django.db.models import Count, Sum
from django.http import HttpResponse

from sites.models import UserSite

def user_statistics(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    user_sites = UserSite.objects.filter(user=request.user).values_list('url', flat=True)
    activities = UserActivity.objects.filter(user=request.user, url__in=user_sites)

    stats = activities.values('url').annotate(
        transitions=Count('id'),
        total_sent=Sum('request_size'),
        total_received=Sum('response_size')
    )

    return render(request, 'stats/stats.html', {'stats': stats})




