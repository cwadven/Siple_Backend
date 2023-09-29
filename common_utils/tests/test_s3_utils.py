import unittest
from unittest.mock import (
    Mock,
    patch,
)
from django.test import TestCase
from botocore.exceptions import NoCredentialsError
from django.conf import settings

from common_utils.s3_utils import generate_presigned_url_info


class TestGeneratePresignedURLInfo(TestCase):
    @patch('common_utils.s3_utils.boto3.client')
    def test_generate_presigned_url_info(self, mock_boto3_client):
        # Given: Set up the test data
        file_name = 'test.txt'
        _type = 'test'
        unique = '123'
        expires_in = 3600

        # Mock the boto3.client and s3_client.generate_presigned_post calls
        mock_s3_client = Mock()
        mock_boto3_client.return_value = mock_s3_client
        mock_generate_presigned_post_response = {
            'url': 'https://s3-bucket-url.com',
            'fields': {
                'key': 'mock-key',
                'AWSAccessKeyId': 'mock-access-key',
                'Policy': 'mock-policy',
                'Signature': 'mock-signature'
            }
        }
        mock_s3_client.generate_presigned_post.return_value = mock_generate_presigned_post_response

        # When: Call the function
        response = generate_presigned_url_info(file_name, _type, unique, expires_in)

        # Then: Assert that s3_client.generate_presigned_post is called with the correct data
        mock_boto3_client.assert_called_once_with(
            's3',
            region_name='ap-northeast-2',
            aws_access_key_id=settings.AWS_IAM_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_IAM_SECRET_ACCESS_KEY,
            config=unittest.mock.ANY  # Ensure that the Config object is created
        )
        mock_s3_client.generate_presigned_post.assert_called_once_with(
            Bucket=settings.AWS_S3_BUCKET_NAME,
            Key=unittest.mock.ANY,  # Ensure the Key is generated with a UUID
            Conditions=[
                ['content-length-range', 0, 10485760]
            ],
            ExpiresIn=expires_in  # Ensure the ExpiresIn parameter is passed correctly
        )

        # Assert the response
        expected_response = mock_generate_presigned_post_response
        self.assertEqual(response, expected_response)

    @patch('common_utils.s3_utils.boto3.client', side_effect=NoCredentialsError())
    def test_generate_presigned_url_info_with_exception(self, mock_boto3_client):
        # Given: Set up the test data
        file_name = 'test.txt'
        _type = 'test'
        unique = '123'
        expires_in = 3600

        # When: Call the function and expect an exception
        with self.assertRaises(Exception):
            generate_presigned_url_info(file_name, _type, unique, expires_in)
