import json
import re
import requests
import datetime

from json.decoder           import JSONDecodeError

from django.http            import JsonResponse
from django.views           import View
from django.conf            import settings
from django.core.exceptions import ValidationError

from accommodations.models import Accommodation
from reservations.models   import Reservation

import jwt
import bcrypt

from users.models           import User
from .validate              import validate_email, validate_password

from users.utils            import login_decorator

class SignUpView(View):
  def post(self,request):
    data = json.loads(request.body)
    try:
      name            = data['name']
      email           = data['email']
      password        = data['password']
      has_agreed      = data['has_agreed']
      hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

      validate_email(email)
      validate_password(password)

      if User.objects.filter(email= email):
        return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)
      
      user = User(
        name       = name,
        email      = email,
        password   = hashed_password,
        has_agreed = has_agreed,
      )

      user.save()
    
      return JsonResponse({'message':'success'}, status=200)

    except KeyError:
      return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    except ValidationError:
      return JsonResponse({'message': 'INVALID_KEY'}, status=400)
      

class KakaoLoginView(View):
  def get(self, request):
    try:
      access_token           = request.headers.get('Authorization')
      kakao_account_response = requests.get('https://kapi.kakao.com/v2/user/me', headers = {'Authorization': f'Bearer {access_token}'}, timeout = 2)

      kakao_account = kakao_account_response.json()
      name     = kakao_account['kakao_account']['profile']['nickname'],
      kakao_id = kakao_account['id']
      email = 'ckdgus1101@naver.com'
      #  email    = kakao_account['kakao_account']['email']

      user, is_created = User.objects.get_or_create(
        name       = name,
        kakao_id   = kakao_id,
        email      = email,
        has_agreed = True
      )
      
      access_token = jwt.encode({'user_id' :  kakao_id}, settings.SECRET_KEY, settings.ALGORITHMS)

      return JsonResponse({"token":access_token, 'message': 'SUCCESS'}, status=200)

    except KeyError:
      return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LogInView(View):
  def post(self, request):
    try:
      data  = json.loads(request.body) 
      user  = User.objects.get(email=data['email'])
      if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return JsonResponse({'message': 'INVALID_PASSWORD'}, status = 401)

      token = jwt.encode({'id': user.id}, settings.SECRET_KEY, settings.ALGORITHMS)
      return JsonResponse({'message':'SUCCESS','token':token}, status=201)

    except KeyError:
      return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    except User.DoesNotExist:
      return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)


class ReservationInfoView(View):
  @login_decorator
  def get(self,request):
    try:
      reservations = Reservation.objects.filter(user_id = request.user).order_by('-created_at')

      result=[{
        'user_id'           : reservation.user_id,
        'accommodation_name': reservation.accommodation.name,
        'price'             : reservation.total_price,
        'check_in_date'     : reservation.check_in,
        'check_out_date'    : reservation.check_out,
        'number_of_adults'  : reservation.number_of_adults,
        'number_of_children': reservation.number_of_children,
        'image_url'         : [image.image_url for image in reservation.accommodation.accommodationimage_set.all()],
      }for reservation in reservations]
      
      return JsonResponse({'result':result},status=200)

    except KeyError:
      return JsonResponse({'message': 'KEY_ERROR'}, stauts=400)