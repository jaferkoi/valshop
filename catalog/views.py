from django.views.generic import ListView, DetailView

from catalog.models import SkinModel


class SkinListView(ListView):
    model = SkinModel
    template_name = 'catalog/skin_list.html'
    context_object_name = 'skins'


class SkinDetailView(DetailView):
    model = SkinModel
    template_name = "catalog/skin_detail.html"
    context_object_name = "skin"
