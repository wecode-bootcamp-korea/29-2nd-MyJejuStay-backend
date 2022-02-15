from django.urls import path, include

urlpatterns = [
    path('accommodations', include('accommodations.urls')),
]
