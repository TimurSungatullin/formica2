from django.urls import path

from .views import *

urlpatterns = [
    path('', ProfilePageInfoView.as_view()),
    path('my_profile', MyProfileView.as_view()),
]
