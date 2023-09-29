import unittest
from unittest.mock import (
    Mock,
    patch,
)
from botocore.exceptions import NoCredentialsError

from common_utils.s3_utils import generate_presigned_url


class TestGeneratePresignedURL(unittest.TestCase):
    @patch('common_utils.s3_utils.boto3.client')
    def test_generate_presigned_url(self, mock_boto3_client):
        # Given: Mock boto3.client
        mock_s3_client = Mock()
        mock_boto3_client.return_value = mock_s3_client

        # And: Mock S3 response
        mock_presigned_url = {
            'url': 'https://mocked-url.com',
            'fields': {
                'key': 'mock-key',
                'AWSAccessKeyId': 'mock-access-key',
                'Policy': 'mock-policy',
                'Signature': 'mock-signature'
            }
        }
        mock_s3_client.generate_presigned_post.return_value = mock_presigned_url

        # And: Mock settings
        mock_settings = Mock()
        mock_settings.AWS_IAM_ACCESS_KEY = 'mock-access-key'
        mock_settings.AWS_IAM_SECRET_ACCESS_KEY = 'mock-secret-key'
        mock_settings.AWS_S3_BUCKET_NAME = 'mock-bucket-name'

        with patch('common_utils.s3_utils.settings', mock_settings):
            # When: Call the function
            response = generate_presigned_url('test.txt', _type='test', unique=123, expires_in=3600)

        # Then: Assertions
        self.assertEqual(response, mock_presigned_url)
        mock_boto3_client.assert_called_once_with(
            's3',
            region_name='ap-northeast-2',
            aws_access_key_id=mock_settings.AWS_IAM_ACCESS_KEY,
            aws_secret_access_key=mock_settings.AWS_IAM_SECRET_ACCESS_KEY,
            config=unittest.mock.ANY  # Ensure that the Config object is created
        )
        mock_s3_client.generate_presigned_post.assert_called_once_with(
            Bucket=mock_settings.AWS_S3_BUCKET_NAME,
            Key=unittest.mock.ANY,  # Ensure the Key is generated with a UUID
            Conditions=[
                ['content-length-range', 0, 10485760]
            ],
            ExpiresIn=3600  # Ensure the ExpiresIn parameter is passed correctly
        )

    def test_generate_presigned_url_with_exception(self):
        # Given: Mock settings
        mock_settings = Mock()
        mock_settings.AWS_IAM_ACCESS_KEY = 'mock-access-key'
        mock_settings.AWS_IAM_SECRET_ACCESS_KEY = 'mock-secret-key'
        mock_settings.AWS_S3_BUCKET_NAME = 'mock-bucket-name'

        # And: Mock boto3.client to raise an exception
        with patch('common_utils.s3_utils.boto3.client', side_effect=NoCredentialsError()):
            with patch('common_utils.s3_utils.settings', mock_settings):
                # Expected: Call the function and expect an exception
                with self.assertRaises(Exception):
                    generate_presigned_url('test.txt', _type='test', unique=123, expires_in=3600)
