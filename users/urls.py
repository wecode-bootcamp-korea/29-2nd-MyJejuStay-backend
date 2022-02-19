from django.urls import path
from .views import SignUpView, KakaoLoginView

urlpatterns = [
  path('/kakaologin', KakaoLoginView.as_view()),
  path('/signup', SignUpView.as_view())
]
