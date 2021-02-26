from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam),
    path('dashboard', views.index),
    path('trips/new', views.new_trip),
    path('trips/create', views.create_trip),
    path('trips/view/<int:num>', views.view_trip),
    path('trips/edit/<int:num>', views.edit_trip),
    path('trips/update/<int:num>', views.update_trip),
    path('trips/delete/<int:num>', views.delete_trip),
    path('trips/join/<int:num>', views.join_trip),
    path('trips/cancel/<int:num>', views.cancel_trip),
]