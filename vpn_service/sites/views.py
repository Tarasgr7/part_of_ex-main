from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from sites.models import UserSite
from django.db.models.functions import Lower
from sites.forms import UserSiteForm
from django.http import HttpResponse
from bs4 import BeautifulSoup
from stats.models import UserActivity
from urllib.parse import urlparse
import requests
import datetime


@login_required
def site_list(request):
    sites = UserSite.objects.filter(user=request.user)
    return render(request, 'sites/site_list.html', {'sites': sites})

@login_required
def site_create(request):
    if request.method == 'POST':
        form = UserSiteForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.user = request.user
            site.save()
            return redirect('site_list')
    else:
        form = UserSiteForm()
    return render(request, 'sites/site_create.html', {'form': form})

def is_internal_link(link, base_url):
    """
    Перевіряє, чи є посилання внутрішнім для базового URL.
    """
    if link.startswith(('mailto:', 'javascript:', '#')):
        return False

    parsed_base = urlparse(base_url)
    parsed_link = urlparse(link)

    return (
        not parsed_link.netloc or  
        parsed_base.netloc == parsed_link.netloc  
    )



@login_required
def proxy_view(request, user_site_name, path=''):
    # Отримати URL сайту користувача
    try:
        user_site = UserSite.objects.get(name=user_site_name, user=request.user)
    except UserSite.DoesNotExist:
        return HttpResponse("Site not found", status=404)


    original_url = user_site.url.rstrip('/') + '/' + path.lstrip('/')
    headers = {
        'User-Agent': request.headers.get('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'),
        'Accept': request.headers.get('Accept', '*/*'),
        'Referer': user_site.url,  # Додайте Referer, якщо це потрібно
    }
    try:
        response = requests.get(original_url, headers=headers, stream=True)
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Failed to fetch site: {e}", status=500)

    content_type = response.headers.get('Content-Type', '')
    content = response.content
    if 'text/html' in content_type:
        soup = BeautifulSoup(response.content, 'html.parser')
        for tag in soup.find_all("a", href=True):
            href = tag.get('href', '')  # Безпечний доступ до href
            if href and is_internal_link(href, user_site.url):  # Перевіряємо, чи посилання валідне
                tag['href'] = f"/{user_site_name}/{href.lstrip('/')}"
        content = str(soup).encode('utf-8')

    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            url=original_url,
            request_size=len(request.body or b""),
            response_size=len(content),
            timestamp=datetime.datetime.now()
        )

    return HttpResponse(content, status=response.status_code, content_type=content_type)



