from django.contrib import admin

# Register your models here.
from achievement.models import Achievement, UserAchievement

admin.site.register(Achievement)
admin.site.register(UserAchievement)