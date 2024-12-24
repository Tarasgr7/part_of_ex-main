from django.conf import settings  # Для використання AUTH_USER_MODEL
from django.db import models

class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=2048)
    request_size = models.BigIntegerField()
    response_size = models.BigIntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user} - {self.url} - {self.timestamp}"
