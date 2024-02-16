from django.contrib.auth.models import AbstractUser

from common.models import ModelBase


class CustomUser(ModelBase, AbstractUser):
    """Custom user class"""

    class Meta:
        
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
