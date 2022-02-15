from django.urls import path

from .views import AccommodationListView, AccommodationView

urlpatterns = [
    path('', AccommodationListView.as_view()),
    path('/<int:accommodation_id>', AccommodationView.as_view()),
]
