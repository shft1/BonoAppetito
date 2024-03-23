from django.contrib.auth.models import AbstractUser
from django.db import models


class UserCustom(AbstractUser):
    pass

    def __str__(self):
        return self.username
