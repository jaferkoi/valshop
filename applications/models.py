from django.db import models
from core.models import BaseModel
from catalog.models import SkinModel


class SkinRequestModel(BaseModel):
    STATUS_NEW = "new"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_NEW, "Новая"),
        (STATUS_APPROVED, "Одобрена"),
        (STATUS_REJECTED, "Отклонена")
    ]
    skin = models.ForeignKey(
        SkinModel,
        on_delete=models.CASCADE,
        related_name="requests",
    )
    nickname = models.CharField(
        verbose_name="Ник в игре",
        max_length=50,
    )
    message = models.CharField(
        verbose_name="Комментарий",
        blank=True,
        max_length=100,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="пользователь",
    )

    def __str__(self):
        return f"Ник: {self.nickname} -> {self.skin}"

    class Meta:
        verbose_name="заявка"
        verbose_name_plural="заявки"
