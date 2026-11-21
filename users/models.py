from django.contrib.auth.models import User as Us
from django.db import models

from applications.models import SkinRequestModel


class User(Us):
    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="пользователь",
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True,
    )
    applications = models.ManyToManyField(
        SkinRequestModel,
        blank=True,
    )
