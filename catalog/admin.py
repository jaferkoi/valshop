from django.contrib import admin
from catalog.models import WeaponModel, SkinModel


@admin.register(WeaponModel)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_published')


@admin.register(SkinModel)
class SkinAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_published')
