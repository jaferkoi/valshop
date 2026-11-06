from django.views.generic import ListView, DetailView

from catalog.models import SkinModel, WeaponModel


class SkinListView(ListView):
    model = SkinModel
    template_name = 'catalog/skin_list.html'
    context_object_name = 'skins'

    def get_queryset(self):
        weapon_slug = self.request.GET.get('weapon')
        self.queryset = super().get_queryset().filter(is_published=True)
        if weapon_slug:
            return self.queryset.filter(weapon__slug=weapon_slug)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weapons'] = WeaponModel.objects.filter(is_published=True)
        return context


class SkinDetailView(DetailView):
    model = SkinModel
    template_name = "catalog/skin_detail.html"
    context_object_name = "skin"

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class WeaponDetailView(DetailView):
    model = WeaponModel
    template_name = "catalog/weapon_detail.html"
    context_object_name = "weapon"

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
