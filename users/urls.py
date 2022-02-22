from django.urls import path
from .views import SignUpView, KakaoLoginView, LogInView, ReservationInfoView

urlpatterns = [
  path('/kakaologin', KakaoLoginView.as_view()),
  path('/signup', SignUpView.as_view()),
  path('/login', LogInView.as_view()),
  path('/reservationinfo', ReservationInfoView.as_view())
]
