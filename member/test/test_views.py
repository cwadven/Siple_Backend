import jwt
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from unittest.mock import (
    Mock,
    patch,
)

from member.consts import SIGNUP_MACRO_COUNT, MemberCreationExceptionMessage
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


class SignUpEmailTokenValidationEndViewTestCase(TestCase):
    def setUp(self):
        super(SignUpEmailTokenValidationEndViewTestCase, self).setUp()
        self.body = {
            'email': 'aaaa@naver.com',
            'one_time_token': '1234',
        }

    @patch('member.views.increase_cache_int_value_by_key')
    def test_email_token_validate_should_return_fail_when_macro_count_is_30_times(self, mock_increase_cache_int_value_by_key):
        # Given: 30 번 메크로를 했을 경우
        mock_increase_cache_int_value_by_key.return_value = 30

        # When:
        response = self.client.post(reverse('member:sign_up_token_validation'), self.body)

        # Then: 메크로 에러
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['message'],
            '{}회 이상 인증번호를 틀리셨습니다. 현 이메일은 {}시간 동안 인증할 수 없습니다.'.format(SIGNUP_MACRO_COUNT, 24)
        )

    @patch('member.views.increase_cache_int_value_by_key')
    @patch('member.views.get_cache_value_by_key')
    def test_email_token_validate_should_return_fail_when_email_key_not_exists(self,
                                                                               mock_get_cache_value_by_key,
                                                                               mock_increase_cache_int_value_by_key):
        # Given: 0 번 메크로를 했을 경우
        mock_increase_cache_int_value_by_key.return_value = 0
        # And: 인증한 이메일이 없는 경우
        mock_get_cache_value_by_key.return_value = None

        # When:
        response = self.client.post(reverse('member:sign_up_token_validation'), self.body)

        # Then: 이메일 에러
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['message'],
            '이메일 인증번호를 다시 요청하세요.',
        )

    @patch('member.views.increase_cache_int_value_by_key')
    @patch('member.views.get_cache_value_by_key')
    def test_email_token_validate_should_return_fail_when_one_time_token_not_exists(self,
                                                                                    mock_get_cache_value_by_key,
                                                                                    mock_increase_cache_int_value_by_key):
        # Given: 0 번 메크로를 했을 경우
        mock_increase_cache_int_value_by_key.return_value = 0
        # And: one time token 이 없는 경우
        mock_get_cache_value_by_key.return_value = {
            'email': 'test@test.com',
            'username': 'test',
            'nickname': 'test',
            'password2': 'test',
        }

        # When:
        response = self.client.post(reverse('member:sign_up_token_validation'), self.body)

        # Then: 인증번호 에러
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['message'],
            '인증번호가 다릅니다.',
        )

    @patch('member.views.increase_cache_int_value_by_key')
    @patch('member.views.get_cache_value_by_key')
    def test_email_token_validate_should_return_fail_when_one_time_token_is_different(self,
                                                                                      mock_get_cache_value_by_key,
                                                                                      mock_increase_cache_int_value_by_key):
        # Given: 0 번 메크로를 했을 경우
        mock_increase_cache_int_value_by_key.return_value = 0
        # And: one time token 다르게 설정
        mock_get_cache_value_by_key.return_value = {
            'one_time_token': '1233',
            'email': 'test@test.com',
            'username': 'test',
            'nickname': 'test',
            'password2': 'test',
        }
        # And: one time token 다르게 설정
        self.body['one_time_token'] = '1234'

        # When:
        response = self.client.post(reverse('member:sign_up_token_validation'), self.body)

        # Then: 인증번호 에러
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['message'],
            '인증번호가 다릅니다.',
        )

    @patch('member.views.increase_cache_int_value_by_key')
    @patch('member.views.get_cache_value_by_key')
    def test_email_token_validate_should_return_fail_when_username_user_already_exists(self,
                                                                                       mock_get_cache_value_by_key,
                                                                                       mock_increase_cache_int_value_by_key):
        # Given: 0 번 메크로를 했을 경우
        mock_increase_cache_int_value_by_key.return_value = 0
        mock_get_cache_value_by_key.return_value = {
            'one_time_token': '1234',
            'email': 'test@test.com',
            'username': 'test',
            'nickname': 'test',
            'password2': 'test',
        }
        # And: 이미 username mocking 한 데이터의 계정이 있는 경우
        Member.objects.create_user(username='test')

        # When:
        response = self.client.post(reverse('member:sign_up_token_validation'), self.body)

        # Then: username 에러
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['message'],
            MemberCreationExceptionMessage.USERNAME_EXISTS.label,
        )

    @patch('member.views.increase_cache_int_value_by_key')
    @patch('member.views.get_cache_value_by_key')
    def test_email_token_validate_should_return_fail_when_nickname_user_already_exists(self,
                                                                                       mock_get_cache_value_by_key,
                                                                                       mock_increase_cache_int_value_by_key):
        # Given: 0 번 메크로를 했을 경우
        mock_increase_cache_int_value_by_key.return_value = 0
        mock_get_cache_value_by_key.return_value = {
            'one_time_token': '1234',
            'email': 'test@test.com',
            'username': 'test',
            'nickname': 'test',
            'password2': 'test',
        }
        # And: 이미 nickname mocking 한 데이터의 계정이 있는 경우
        Member.objects.create_user(username='test2', nickname='test')

        # When:
        response = self.client.post(reverse('member:sign_up_token_validation'), self.body)

        # Then: 닉네임 중복 에러
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['message'],
            MemberCreationExceptionMessage.NICKNAME_EXISTS.label,
        )

    @patch('member.views.increase_cache_int_value_by_key')
    @patch('member.views.get_cache_value_by_key')
    def test_email_token_validate_should_return_fail_when_email_user_already_exists(self,
                                                                                    mock_get_cache_value_by_key,
                                                                                    mock_increase_cache_int_value_by_key):
        # Given: 0 번 메크로를 했을 경우
        mock_increase_cache_int_value_by_key.return_value = 0
        mock_get_cache_value_by_key.return_value = {
            'one_time_token': '1234',
            'email': 'test@test.com',
            'username': 'test',
            'nickname': 'test',
            'password2': 'test',
        }
        # And: 이미 email mocking 한 데이터의 계정이 있는 경우
        Member.objects.create_user(username='test2', nickname='test2', email='test@test.com')

        # When:
        response = self.client.post(reverse('member:sign_up_token_validation'), self.body)

        # Then: email 중복 에러
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['message'],
            MemberCreationExceptionMessage.EMAIL_EXISTS.label,
        )

    @patch('member.views.delete_cache_value_by_key', Mock())
    @patch('member.views.increase_cache_int_value_by_key')
    @patch('member.views.get_cache_value_by_key')
    def test_email_token_validate_should_return_success(self,
                                                        mock_get_cache_value_by_key,
                                                        mock_increase_cache_int_value_by_key):
        # Given: 0 번 메크로를 했을 경우
        mock_increase_cache_int_value_by_key.return_value = 0
        mock_get_cache_value_by_key.return_value = {
            'one_time_token': '1234',
            'email': 'test@test.com',
            'username': 'test',
            'nickname': 'test',
            'password2': 'test',
        }

        # When:
        response = self.client.post(reverse('member:sign_up_token_validation'), self.body)

        # Then: 성공
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['message'],
            '회원가입에 성공했습니다.',
        )
        self.assertEqual(
            Member.objects.filter(email=mock_get_cache_value_by_key.return_value['email']).exists(),
            True
        )
