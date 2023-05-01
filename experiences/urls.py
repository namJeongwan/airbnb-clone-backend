from django.urls import path
from . import views

urlpatterns = [
    path("", views.ExperienceList.as_view()),
    path("<int:pk>/", views.ExperienceDetail.as_view()),
    path("perks/", views.Perks.as_view()),
    path("perks/<int:pk>", views.PerksDetail.as_view()),
    path("<int:pk>/perks/", views.ExperiencePerks.as_view()),
    path("<int:pk>/bookings/", views.ExperienceBookings.as_view()),
]