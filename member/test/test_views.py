import jwt
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

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
            'user_id': self.member.id,
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
