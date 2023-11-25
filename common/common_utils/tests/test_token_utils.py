from datetime import datetime
from django.test import TestCase
from unittest.mock import patch

from freezegun import freeze_time

from common.common_utils.token_utils import (
    get_jwt_login_token,
    get_jwt_refresh_token,
)
from member.models import Member


class TestGetJWTLoginToken(TestCase):
    def setUp(self):
        self.member = Member.objects.all().first()

    @patch('common.common_utils.token_utils.jwt_payload_handler')
    @patch('common.common_utils.token_utils.jwt_encode_handler')
    def test_get_jwt_login_token(self, mock_jwt_encode_handler, mock_jwt_payload_handler):
        # Given:
        # When:
        get_jwt_login_token(self.member)

        # Then: Ensure the function executes and returns the expected result
        mock_jwt_payload_handler.assert_called_once_with(self.member)
        mock_jwt_encode_handler.assert_called_once_with(mock_jwt_payload_handler.return_value)


class TestGetJWTRefreshToken(TestCase):
    def setUp(self):
        self.member = Member.objects.all().first()

    @freeze_time('2020-01-01 00:00:00')
    @patch('common.common_utils.token_utils.jwt_encode_handler')
    def test_get_jwt_refresh_token(self, mock_jwt_encode_handler):
        # Given:
        # When:
        get_jwt_refresh_token(self.member)

        # Then: Ensure the function executes and returns the expected result
        mock_jwt_encode_handler.assert_called_once_with({
            'member_id': self.member.id,
            'exp': datetime(2020, 1, 8)
        })
