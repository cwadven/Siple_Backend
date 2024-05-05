import base64
import json

from common.common_utils.decode_utils import urlsafe_base64_to_data
from django.test import TestCase


class TestUrlSafeBase64ToData(TestCase):
    def test_base64_to_data_conversion(self):
        # Given: 원본 데이터
        original_data = {'name': '홍길동', 'age': 30}
        # And: 데이터를 JSON으로 변환 후 base64 인코딩
        json_str = json.dumps(original_data)
        json_bytes = json_str.encode('utf-8')
        base64_str = base64.urlsafe_b64encode(json_bytes).decode('utf-8')

        # When: 테스트 대상 함수 실행
        result = urlsafe_base64_to_data(base64_str)

        # Then: 변환된 데이터가 원본 데이터와 같은지 확인
        self.assertEqual(result, original_data)
