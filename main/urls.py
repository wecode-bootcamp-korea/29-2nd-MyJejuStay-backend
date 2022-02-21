from django.urls import path
from .views      import PageVideoView

urlpatterns = {
  path('', PageVideoView.as_view())
}