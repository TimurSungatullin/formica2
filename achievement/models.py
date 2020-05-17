import os

from django.db import models
from django.utils.timezone import now

from formica.settings import ACHIEVEMENT_DIR_NAME


class Achievement(models.Model):

    def path(instance, filename):
        return os.path.join(ACHIEVEMENT_DIR_NAME, instance.title,
                            filename)

    title = models.CharField(
        max_length=50,
        verbose_name='Название',
    )

    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )

    created = models.DateTimeField(
        default=now,
        verbose_name='Дата'
    )

    picture = models.FileField(
        verbose_name='Картинка',
        upload_to=path,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'


class UserAchievement(models.Model):

    # Ачивка пользотелю не за цель, а за другие заслуги
    profile = models.ForeignKey(
        'profile_page.Profile',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        null=True,
        blank=True,
    )

    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.PROTECT,
        verbose_name='Достижение'
    )

    created = models.DateTimeField(
        default=now,
        verbose_name='Дата',
    )

    # Ачивка пользователю за цель
    user_aim = models.ForeignKey(
        'aim.UserAim',
        on_delete=models.CASCADE,
        verbose_name='Цель пользователя',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижения пользователей'
