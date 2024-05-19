from django.contrib.auth.models import AbstractUser
from django.db import models


class UserCustom(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    user = models.ForeignKey(
        UserCustom,
        on_delete=models.CASCADE,
        related_name='follow',
        verbose_name='Подписчик'
    )
    follow = models.ForeignKey(
        UserCustom,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь'
    )

    def __str__(self):
        return f'Подписчик: {self.user} - Пользователь: {self.follow}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
