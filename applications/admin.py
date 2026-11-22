from django.contrib import admin
from applications.models import SkinRequestModel


@admin.register(SkinRequestModel)
class SkinRequestAdmin(admin.ModelAdmin):
    list_display=("nickname", "skin", "status", "created_at")
    list_filter=("status",)
    search_fields=("nickname", "skin__name")
    readonly_fields=("user",)

    @admin.action(description="✅ Одобрить заявки")
    def approve(self, request, queryset):
        queryset.update(status=SkinRequestModel.STATUS_APPROVED)

    @admin.action(description="❌ Отклонить заявки")
    def reject(self, request, queryset):
        queryset.update(status=SkinRequestModel.STATUS_REJECTED)

    actions = ('approve', 'reject')