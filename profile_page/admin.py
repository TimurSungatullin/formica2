from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profile_page.forms import ProfileChange
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(UserAdmin):

    form = ProfileChange
    fieldsets = None
