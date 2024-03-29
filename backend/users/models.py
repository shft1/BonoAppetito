from django.contrib.auth.models import AbstractUser
from django.db import models


class UserCustom(AbstractUser):
    email = models.EmailField('Адрес электронной почты',
                              max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        UserCustom,
        on_delete=models.CASCADE,
        related_name='follow',
    )
    follow = models.ForeignKey(
        UserCustom,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
