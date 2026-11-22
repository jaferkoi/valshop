from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib import messages

from catalog.models import SkinModel, WeaponModel
from applications.forms import SkinRequestForm


class SkinListView(ListView):
    model = SkinModel
    template_name = 'catalog/skin_list.html'
    context_object_name = 'skins'
    paginate_by = 6

    def get_queryset(self):
        weapon_slug = self.request.GET.get('weapon')
        queryset = super().get_queryset().filter(
            is_published=True,
            weapon__is_published=True,
        ).select_related("weapon")
        if weapon_slug:
            return queryset.filter(weapon__slug=weapon_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weapons'] = WeaponModel.objects.filter(is_published=True)
        return context


class SkinDetailView(LoginRequiredMixin, DetailView):
    model = SkinModel
    template_name = "catalog/skin_detail.html"
    context_object_name = "skin"

    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
            weapon__is_published=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = kwargs.get("form")
        if not form:
            form = SkinRequestForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = SkinRequestForm(request.POST)
        if form.is_valid():
            skin_request = form.save(commit=False)
            skin_request.skin = self.get_object()
            skin_request.user = request.user
            skin_request.save()
            messages.success(request, "Заявка успешно отправлена")
            return redirect("catalog:skin_list")
        else:
            return self.render_to_response(self.get_context_data(form=form))


class WeaponDetailView(DetailView):
    model = WeaponModel
    template_name = "catalog/weapon_detail.html"
    context_object_name = "weapon"

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skins"] = self.object.skins.filter(is_published=True)
        return context
