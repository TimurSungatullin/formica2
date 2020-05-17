import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(User):
    """Модель профиля пользователя"""

    def path(instance, filename):
        return os.path.join(instance.last_name + instance.first_name,
                            filename)

    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения',
    )

    info = models.TextField(
        default='',
        verbose_name='Информация о пользователе',
        null=True,
        blank=True,
    )

    bio = models.TextField(
        default='',
        verbose_name='Происхождение пользователя',
        null=True,
        blank=True,
    )

    is_prime = models.BooleanField(
        default=False,
        verbose_name='Есть ли подписка',
    )

    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        blank=True,
        null=True,
    )

    city = models.CharField(
        max_length=100,
        verbose_name='Город',
        blank=True,
        null=True,
    )

    friend = models.ManyToManyField(
        'self',
        verbose_name='Друзья',
        null=True,
        blank=True,
    )

    avatar = models.FileField(
        upload_to=path,
        null=True,
        blank=True,
        verbose_name='Аватар',
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = Profile(**values)
        user.save()
