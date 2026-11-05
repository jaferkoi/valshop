from django.urls import path
from . import views


app_name = "catalog"

urlpatterns = [
    path('', views.SkinListView.as_view(), name="skin_list"),
    path('<slug:slug>/', views.SkinDetailView.as_view, name="skin_detail")
]
