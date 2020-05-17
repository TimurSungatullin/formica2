from django.contrib.auth.backends import ModelBackend

from profile_page.models import Profile


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Profile.objects.get(username=username)
            if user.check_password(password):
                # Теперь в request лежит Profile, а не User
                return user
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None
