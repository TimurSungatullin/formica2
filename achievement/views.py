from django.forms import model_to_dict

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserAchievement


class GetUserAchievmentsView(APIView):

    def get(self, request):

        profile_id = request.GET.get('profile_id', None)
        if profile_id is None:
            return Response(status=400, data='No profile_id in kwargs!')

        user_achievements = UserAchievement.objects.filter(
            profile__id=profile_id).select_related('achievement')
        data = []
        for user_achievement in user_achievements:
            model_entry = {
                'user_achievement': model_to_dict(user_achievement),
                'achievement': model_to_dict(user_achievement.achievement, exclude=('picture',)),
                'user_aim': (
                    model_to_dict(user_achievement.user_aim, exclude=('picture',))
                        if user_achievement.user_aim is not None
                            else None),
            }
            data.append(model_entry)

        return Response(status=200, data=data)

    def post(self, request):
        pass