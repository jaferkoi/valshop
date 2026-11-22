from django.db import models

from core.models import SlugModel


class WeaponModel(SlugModel):
    name = models.CharField(
        verbose_name="название",
        help_text="Название не должно превышать 30 символов",
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="оружие"
        verbose_name_plural="оружие"


class SkinModel(SlugModel):
    name = models.CharField(
        verbose_name="скин",
        help_text="Название скина не должно превышать 20 символов",
        max_length=20,
    )
    weapon = models.ForeignKey(
        WeaponModel,
        on_delete=models.CASCADE,
        related_name="skins"
    )
    image = models.ImageField(
        upload_to="skins/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name="скин"
        verbose_name_plural="скины"
        ordering=("name",)

    def __str__(self):
        return f"Скин: {self.name} -> {self.weapon}"
