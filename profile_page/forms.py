from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UsernameField

from profile_page.models import Profile


class ProfileChange(UserChangeForm):

    class Meta:
        model = Profile
        fields = '__all__'
        field_classes = {'username': UsernameField}
