from django.db import models
from django.conf import settings

class UserSite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sites")
    name = models.CharField(max_length=100)
    url = models.URLField()
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
