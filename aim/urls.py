from django.urls import path

from .views import *

urlpatterns = [
    path('', GetAimView.as_view()),
    path('get_all_aims', GetUserAimsView.as_view()),
    path('user_aim', UserAimView.as_view()),
]
