import datetime

from django.forms import model_to_dict

from rest_framework.views import APIView
from rest_framework.response import Response

from aim.helpers import set_values_to_model
from aim.models import UserAim, Aim
from profile_page.models import Profile


class GetUserAimsView(APIView):
    """Получалка всех целей у пользователя"""

    def get(self, request):

        profile_id = request.GET.get('profile_id', None)
        if profile_id is None:
            return Response(status=400, data='No profile_id in kwargs!')

        user_aims = UserAim.objects.filter(
            profile__id=profile_id).select_related('aim')
        data = []
        for user_aim in user_aims:
            model_entry = {
                'user_aim': model_to_dict(user_aim),
                'aim': model_to_dict(user_aim.aim, exclude=('picture',))
            }
            data.append(model_entry)

        return Response(status=200, data=data)


class GetAimView(APIView):
    """Чтение одной цели"""

    def get(self, request):

        aim_id = request.GET.get('aim_id', None)
        if aim_id is None:
            return Response(status=400, data='No aim_id in kwargs!')
        try:
            aim = Aim.objects.get(id=aim_id)
        except Aim.DoesNotExist:
            return Response(status=400, data='We havent got aim with this id')

        return Response(status=200, data=model_to_dict(aim, exclude=('picture',)))


class UserAimView(APIView):
    """Чтение/запись одной цели у пользователя"""

    def get(self, request):

        aim_id = request.GET.get('aim_id', None)
        if aim_id is None:
            return Response(status=400, data='No aim_id in kwargs!')
        try:
            user_aim = UserAim.objects.get(aim_id=aim_id)
        except UserAim.DoesNotExist:
            return Response(status=400, data='We havent got aim with this id')

        return Response(status=200, data={
            'user_aim': model_to_dict(user_aim, exclude=('aim',)),
            'aim': model_to_dict(user_aim.aim, exclude=('picture',)),
        })

    def post(self, request):

        # Если user_aim_id None тогда создается новая цель
        user_aim_id = request.POST.get('user_aim_id', None)
        author_id = request.POST.get('author_id', None)
        profile = None
        if author_id is not None:
            profile = Profile.objects.get(id=author_id)
        user_aim = (UserAim.objects.get(id=user_aim_id)
                    if user_aim_id is not None else UserAim())

        aim = (user_aim.aim if user_aim_id is not None else Aim())

        # UserAim
        regularity = request.POST.get('regularity', None)
        deadline = request.POST.get('deadline', None)
        completed = request.POST.get('completed', None) == 'True'
        user_aim_fields = {
            'deadline': (datetime.datetime.strptime(deadline, '%Y-%m-%dT%H:%M:%S')
                            if deadline is not None else None),
            'is_closed': request.POST.get('is_closed', None) == 'True',
            'regularity': int(regularity) if regularity else None,
            'completed': datetime.datetime.now() if completed else None,
            'profile': profile,
            'aim': aim,
        }
        # Aim
        rate = request.POST.get('rate', None)
        aim_fields = {
            'title': request.POST.get('title', None),
            'info': request.POST.get('info', None),
            'rate': int(rate) if rate is not None else None,
            'author': profile,
        }

        set_values_to_model(aim, aim_fields)
        set_values_to_model(user_aim, user_aim_fields)

        return Response(status=200, data={
            'user_aim': model_to_dict(user_aim, exclude=('aim',)),
            'aim': model_to_dict(user_aim.aim, exclude=('picture',)),
        })
