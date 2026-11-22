from django.views.generic import ListView

from catalog.models import SkinModel


class HomeView(ListView):
    model = SkinModel
    template_name = "homepage/index.html"
    context_object_name = "skins"

    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
            weapon__is_published=True,
        ).select_related("weapon").order_by("-created_at")[:3]
