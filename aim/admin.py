from django.contrib import admin

from aim.models import Aim
from aim.models import UserAim

admin.site.register(Aim)
admin.site.register(UserAim)
