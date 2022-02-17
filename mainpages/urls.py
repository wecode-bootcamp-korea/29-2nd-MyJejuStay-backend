from django.urls import path
from .views      import MainPageView
urlpatterns = {
  path('mainpage', MainPageView.as_view())
}