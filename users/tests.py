import jwt, datetime

from django.test    import TestCase, Client
from django.conf    import settings
from unittest       import mock
from unittest.mock  import patch

from .models   import User
from accommodations.models import Accommodation, AccommodationImage
from reservations.models import Reservation
class KakaoSignInTest(TestCase):
    def setUp(self):
        User.objects.create(
			kakao_id = 2145645622,
            email    = 'ckdgus1101@naver.com',
            name = '홍길동'
        )

    def tearDown(self):
        User.objects.all().delete()
    
    @patch("users.views.requests")
    def test_kakao_login_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                  'result':{
                    "id": 2145645622,
                    "kakao_account": { 
                      'email': 'ckdgus1101@naver.com',
                      "profile": {
                            "nickname": "홍길동",
                      }
                    }
                  }
                }

        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "access token"}
        response            = client.get("/users/kakaologin", **headers)
        access_token        = jwt.encode({'user_id' : 1}, settings.SECRET_KEY, settings.ALGORITHMS)

        print(response.json())
        self.assertEqual(response.status_code, 200 or 201)
        self.assertEqual(response.json(),{
          'token': access_token,
        })

    @patch('users.views.requests')
    def test_kakao_login_key_error(self, mocked_requests):
      client = Client()
      class MockedResponse:
        def json(self):
          return {
          }

      mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
      headers             = {"HTTP_Authorization" : "a123423423412341234"}
      response            = client.get("/users/kakaologin", **headers)

      self.assertEqual(response.status_code, 400)

class UserMyPageViewTest(TestCase):
  def setup(self):
    user = User.objects.create(
      id         = 1,
      name       = '최창현',
      email      = 'test@email.com',
      kakao_id   = 1231412,
      has_agreed = True,
    )

    accommodation = Accommodation.objects.create(
      id                 = 1,
      name               = 'test_name',
      description        = 'test_description',
      price              = 1,
      address            = 'test_address',
      region             = 'test_region',
      is_verified        = True,
      latitue            = 1,
      longtitude         = 1,
      check_in_time      = '14:00',
      check_out_time     = '11:00',
      minimun_stay       = 1,
      detail_description = 'test_detail_description',
      avilable_people    = 1
    )

    accommodationimage = AccommodationImage.objects.create(
      id               = 1,
      accommodation_id = 1,
      image_url        = 'test_image_url'
    )

    reservation = Reservation.objects.create(
      id                 = 1,
      user_id            = 1,
      accommodation_id   = 1,
      check_in           = '2022. 2. 24 오전 9:00:00',
      check_out          = '2022. 2. 24 오전 9:00:00',
      number_of_adults   = 1,
      number_of_children = 1,
      reservation_code   = 1,
      total_price        = 1,
      created_at         = 1
    )

  def test_success_user_my_page_view_get_method(self):
    client   = Client()
    # user  = {"Authorization" : "1"}
    response = client.get('/users/mypage')
    print(response.json())
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(),{
      'result': [{
        'user_id'           : '1',
        'accommodation_name': 'test_name',
        'price'             : 'test_price',
        'check_in_date'     : '2022. 2. 24 오전 9:00:00',
        'check_out_date'    : '2022. 2. 24 오전 9:00:00',
        'number_of_adults'  : 1,
        'number_of_children': 1,
        'image_url'         : 'test_image_url'}
      ]
    })
  





      


