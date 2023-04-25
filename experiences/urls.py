from django.urls import path
from .views import Perks, PerksDetail

urlpatterns = [
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerksDetail.as_view()),
]