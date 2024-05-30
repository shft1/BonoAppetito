from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTHS = 150


class UserModel(AbstractUser):
    email = models.EmailField(
        max_length=MAX_LENGTHS,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=MAX_LENGTHS,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTHS,
        verbose_name='Фамилия'
    )
    subscribe = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Subscription',
        related_name='followers',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


User = get_user_model()


class Subscription(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_subscribe',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_followers',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'Подписчик: {self.follower} - Пользователь: {self.following}'
