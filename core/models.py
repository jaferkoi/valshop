from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="создано в",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="обновлено в"
    )
    is_published = models.BooleanField(
        verbose_name="опубликовано",
        default=True,
    )

    class Meta:
        abstract = True


class SlugModel(BaseModel):
    slug = models.SlugField(
        verbose_name="слаг",
        unique=True,
        max_length=64,
        allow_unicode=True,
    )

    class Meta:
        abstract = True
