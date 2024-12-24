import datetime
from django.utils.deprecation import MiddlewareMixin
from stats.models import UserActivity

class TrafficMonitorMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = datetime.datetime.now()

    def process_response(self, request, response):
        if hasattr(request, "start_time"):
            user = request.user if request.user.is_authenticated else None
            url = request.path
            request_size = len(request.body or b"")
            response_size = len(response.content or b"")
            UserActivity.objects.create(
                user=user,
                url=url,
                request_size=request_size,
                response_size=response_size,
                timestamp=datetime.datetime.now()
            )
        return response
