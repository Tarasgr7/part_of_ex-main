from django.contrib import admin
from .models import UserActivity

@admin.register(UserActivity)
class UsageStatAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'request_size', 'response_size', 'timestamp')  # Справжні поля моделі
    list_filter = ('user', 'timestamp')  # Справжні поля моделі
