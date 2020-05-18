import datetime

from django.forms import model_to_dict
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response

from aim.helpers import set_values_to_model
from aim.models import UserAim, Aim
from profile_page.models import Profile


class GetUserAimsView(APIView):
    """Получалка всех целей у пользователя"""

    permission_classes = [IsAuthenticated]

    def get(self, request):

        profile_id = request.GET.get('profile_id', None)
        if profile_id is None:
            profile_id = request.user.id

        user_aims = UserAim.objects.filter(
            profile__id=profile_id).select_related('aim')
        data = []
        for user_aim in user_aims:
            model_entry = {
                'user_aim': model_to_dict(user_aim),
            }
            model_entry['user_aim']['aim'] = model_to_dict(
                user_aim.aim,
                exclude=('picture',)
            )
            data.append(model_entry)

        return Response(status=200, data=data)


class GetAimView(APIView):
    """Апи для целей"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Чтение цели или целей"""
        aim_id = request.GET.get('aim_id', None)
        if aim_id is None:
            # Если id нет, то читаем все
            aims = Aim.objects.all()
            data = []
            for aim in aims:
                row = {
                    'aim': model_to_dict(aim, exclude=('picture',))
                }
                row['aim']['author'] = model_to_dict(
                    aim.author,
                    exclude=('password', 'avatar')
                )
                data.append(row)
            response = Response(status=200, data=data)
        else:
            try:
                aim = Aim.objects.get(id=aim_id)
                data = model_to_dict(aim, exclude=('picture',))
                data['author'] = model_to_dict(
                    aim.author,
                    exclude=('password', 'avatar')
                )
                response = Response(status=200, data=model_to_dict(aim, exclude=('picture',)))
            except Aim.DoesNotExist:
                response = Response(status=400, data="We haven't got aim with this id")

        return response

    def post(self, request):
        """Создание или обновление цели"""
        aim_id = request.POST.get('aim_id', None)
        title = request.POST.get('title', None)
        info = request.POST.get('info', None)
        if aim_id:
            try:
                aim = Aim.objects.get(id=aim_id)
            except Aim.DoesNotExist:
                return Response(status=400,
                                data="We haven't got aim with this id")
        else:
            aim = Aim()
        aim_fields = {
            'title': title,
            'info': info
        }
        if aim_id is None:
            aim_fields.update({
                'author_id': request.user.id
            })

        set_values_to_model(aim, aim_fields)
        data = model_to_dict(aim, exclude=('picture',))
        data['author'] = model_to_dict(
            aim.author,
            exclude=('password', 'avatar'),
        )
        return Response(status=200, data=data)


class UserAimView(APIView):
    """Чтение/запись одной цели у пользователя"""

    permission_classes = [IsAuthenticated]

    def get(self, request):

        aim_id = request.GET.get('aim_id', None)
        profile_id = request.GET.get('profile_id', None)
        if aim_id is None:
            return Response(status=400, data='No aim_id in kwargs!')
        if profile_id is None:
            profile_id = request.user.id
        try:
            user_aim = UserAim.objects.get(aim_id=aim_id, profile_id=profile_id)
        except UserAim.DoesNotExist:
            return Response(status=400, data="We haven't got aim with this id")

        data = model_to_dict(user_aim)
        data['aim'] = model_to_dict(
            user_aim.aim,
            exclude=('picture', )
        )
        data['aim']['author'] = model_to_dict(
            user_aim.aim.author,
            exclude=('password', 'avatar'),
        )
        return Response(status=200, data=data)

    def post(self, request):

        # Если user_aim_id None тогда создается новая цель
        # TODO: Если Post пустой, то он создаст пустую цель
        user_aim_id = request.POST.get('user_aim_id', None)
        # Если есть aim, то цель выбрана из select
        aim_id = request.POST.get('aim_id', None)
        profile_id = request.user.id
        if user_aim_id:
            try:
                user_aim = UserAim.objects.get(id=user_aim_id)
            except UserAim.DoesNotExist:
                return Response(status=400,
                                data="We haven't got user aim's with this id")
        else:
            user_aim = UserAim()

        if aim_id:
            try:
                aim = Aim.objects.get(id=aim_id)
            except Aim.DoesNotExist:
                return Response(status=400,
                                data="We haven't got aim with this id")
        elif user_aim_id:
            aim = user_aim.aim
        else:
            aim = Aim()

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
            'profile_id': profile_id,
            'aim': aim,
        }
        # Aim
        title = request.POST.get('title', None)
        info = request.POST.get('info', None)
        aim_fields = {}
        if any((title, info)):
            aim_fields.update({
                'title': request.POST.get('title', None),
                'info': request.POST.get('info', None),
            })
        if aim_id is None:
            # Если создаётся новая цель, то Автор
            # текущий пользователь
            aim_fields.update({
                'author_id': profile_id
            })

        set_values_to_model(aim, aim_fields)
        set_values_to_model(user_aim, user_aim_fields)

        data = model_to_dict(user_aim)
        data['aim'] = model_to_dict(
            user_aim.aim,
            exclude=('picture', )
        )
        data['aim']['author'] = model_to_dict(
            user_aim.aim.author,
            exclude=('password', 'avatar'),
        )

        return Response(status=200, data=data)
