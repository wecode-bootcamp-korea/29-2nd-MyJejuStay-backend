from django.urls import path, include

urlpatterns = [
  path('users', include('users.urls')),
  path('accommodations', include('accommodations.urls')),
  path('video', include('main.urls')),
]
