import jwt
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from unittest.mock import (
    Mock,
    patch,
)

from member.models import Member


class SocialLoginViewTestCase(TestCase):
    def setUp(self):
        self.member = Member.objects.all().first()
        self.url = reverse('member:social_login')

    @patch('member.views.Member.objects.get_or_create_member_by_token')
    @patch('member.views.Member.raise_if_inaccessible')
    @patch('member.views.login')
    @patch('member.views.get_jwt_login_token')
    @patch('member.views.get_jwt_refresh_token')
    def test_social_login(self, mock_get_jwt_refresh_token, mock_get_jwt_login_token, mock_login, mock_raise_if_inaccessible, mock_get_or_create_member_by_token):
        # Given: test data
        data = {
            'provider': 0,
            'token': 'test_token',
        }
        mock_get_jwt_login_token.return_value = 'test_access_token'
        mock_get_jwt_refresh_token.return_value = 'test_refresh_token'
        mock_get_or_create_member_by_token.return_value = (self.member, True)

        # When
        response = self.client.post(self.url, data, format='json')

        # Then
        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response data for expected keys
        mock_login.called_once()
        mock_raise_if_inaccessible.called_once()
        self.assertEqual(response.data['access_token'], 'test_access_token')
        self.assertEqual(response.data['refresh_token'], 'test_refresh_token')
        self.assertEqual(response.data['is_created'], True)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.member = Member.objects.all().first()
        self.url = reverse('member:normal_login')

    @patch('member.views.login')
    @patch('member.views.get_jwt_login_token')
    @patch('member.views.get_jwt_refresh_token')
    @patch('member.views.authenticate')
    def test_login_when_success(self, mock_authenticate, mock_get_jwt_refresh_token, mock_get_jwt_login_token, mock_login):
        # Given: test data
        data = {
            'username': 'test_username',
            'password': 'test_password',
        }
        mock_get_jwt_login_token.return_value = 'test_access_token'
        mock_get_jwt_refresh_token.return_value = 'test_refresh_token'
        # And: set the mock member
        mock_authenticate.return_value = self.member

        # When
        response = self.client.post(self.url, data, format='json')

        # Then
        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response data for expected keys
        mock_login.called_once()
        self.assertEqual(response.data['access_token'], 'test_access_token')
        self.assertEqual(response.data['refresh_token'], 'test_refresh_token')

    @patch('member.views.authenticate')
    def test_login_when_fail_with_not_member_exists(self, mock_authenticate):
        # Given: test data
        data = {
            'username': 'test_username',
            'password': 'test_password',
        }
        # And: set the mock member as None
        mock_authenticate.return_value = None

        # When
        response = self.client.post(self.url, data, format='json')

        # Then
        # Check the response status code
        self.assertEqual(response.status_code, 400)

        # Check the response data for expected keys
        self.assertEqual(response.data['message'], '아이디 및 비밀번호 정보가 일치하지 않습니다.')


class RefreshTokenViewViewTestCase(TestCase):
    def setUp(self):
        self.member = Member.objects.all().first()
        self.url = reverse('member:refresh_token')

    @patch('member.views.jwt_decode_handler')
    @patch('member.views.get_jwt_refresh_token')
    @patch('member.views.get_jwt_login_token')
    def test_refresh_token_when_success(self, mock_get_jwt_login_token, mock_get_jwt_refresh_token, mock_jwt_decode_handler):
        # Given: test data
        data = {
            'refresh_token': 'test_refresh_token',
        }
        mock_jwt_decode_handler.return_value = {
            'member_id': self.member.id,
        }
        mock_get_jwt_login_token.return_value = 'test_jwt_login_token'
        mock_get_jwt_refresh_token.return_value = 'test_jwt_refresh_token'

        # When
        response = self.client.post(self.url, data, format='json')

        # Then
        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response data for expected keys
        self.assertEqual(response.data['access_token'], 'test_jwt_login_token')
        self.assertEqual(response.data['refresh_token'], 'test_jwt_refresh_token')

    @patch('member.views.jwt_decode_handler')
    def test_refresh_token_fail_with_member_not_exists(self, mock_jwt_decode_handler):
        # Given: test data
        data = {
            'refresh_token': 'test_refresh_token',
        }
        # And: set the mock member as not exists
        mock_jwt_decode_handler.return_value = {
            'member_id': 0,
        }

        # When
        response = self.client.post(self.url, data, format='json')

        # Then
        # Check the response status code
        self.assertEqual(response.status_code, 401)

        # Check the response data for expected keys
        self.assertEqual(response.data['message'], '잘못된 리프레시 토큰입니다.')

    @patch('member.views.jwt_decode_handler')
    def test_refresh_token_fail_with_jwt_invalid(self, mock_jwt_decode_handler):
        # Given: test data
        data = {
            'refresh_token': 'test_refresh_token',
        }
        # And: set the mock member as not exists
        mock_jwt_decode_handler.side_effect = jwt.InvalidTokenError('test_exception')

        # When
        response = self.client.post(self.url, data, format='json')

        # Then
        # Check the response status code
        self.assertEqual(response.status_code, 401)

        # Check the response data for expected keys
        self.assertEqual(response.data['message'], '잘못된 리프레시 토큰입니다.')


class SignUpEmailTokenSendTestCase(TestCase):
    def setUp(self):
        super(SignUpEmailTokenSendTestCase, self).setUp()
        self.body = {
            'username': 'test',
            'nickname': 'test_token',
            'password2': '12341234123412341234',
            'email': 'aaaa@naver.com',
        }

    @patch('member.views.send_one_time_token_email')
    @patch('member.views.get_cache_value_by_key')
    @patch('member.views.generate_random_string_digits')
    def test_email_token_create_when_token_create_successful(self, mock_generate_random_string_digits, mock_get_cache_value_by_key, mock_send_one_time_token_email):
        # Given:
        mock_generate_random_string_digits.return_value = '1234'
        mock_get_cache_value_by_key.return_value = {
            'one_time_token': mock_generate_random_string_digits.return_value,
            'email': self.body['email'],
            'username': self.body['username'],
            'nickname': self.body['nickname'],
            'password2': self.body['password2'],
        }

        # When:
        response = self.client.post(reverse('member:sign_up_check'), self.body)

        # Then: 성공 했다는 메시지 반환
        self.assertEqual(response.status_code, 200)
        mock_send_one_time_token_email.apply_async.assert_called_once_with(
            (
                self.body['email'],
                mock_get_cache_value_by_key.return_value['one_time_token'],
            )
        )
        self.assertEqual(response.data['message'], '인증번호를 이메일로 전송했습니다.')
        # And: cache 에 값이 저장되었는지 확인
        self.assertDictEqual(cache.get(self.body['email']), mock_get_cache_value_by_key.return_value)

    @patch('member.views.generate_dict_value_by_key_to_cache', Mock())
    @patch('member.views.send_one_time_token_email')
    @patch('member.views.get_cache_value_by_key')
    def test_email_token_create_when_token_create_failed(self, mock_get_cache_value_by_key, mock_send_one_time_token_email):
        # Given:
        mock_get_cache_value_by_key.return_value = None

        # When:
        response = self.client.post(reverse('member:sign_up_check'), self.body)

        # Then: 실패 했다는 메시지 반환
        self.assertEqual(response.status_code, 400)
        mock_send_one_time_token_email.assert_not_called()
        self.assertEqual(response.data['message'], '인증번호를 이메일로 전송하지 못했습니다.')
