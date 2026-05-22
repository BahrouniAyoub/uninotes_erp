from django.urls import path

from . import views

urlpatterns = [
    path("basket/", views.basket_view, name="basket"),
    path("basket/add/<int:module_id>/", views.add_module_view, name="add_module"),
    path("basket/remove/<int:module_choisi_id>/", views.remove_module_view, name="remove_module"),
]