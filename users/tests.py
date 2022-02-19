import jwt, datetime

from django.test    import TestCase, Client
from django.conf    import settings
from unittest       import mock
from unittest.mock  import patch

from .models   import User

class KakaoSignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
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
      
