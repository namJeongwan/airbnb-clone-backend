from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:pk>/", views.RoomDetail.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>/", views.AmenityDetail.as_view()),
]