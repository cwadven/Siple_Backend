from datetime import date

from common.common_testcase_helpers.job.testcase_helpers import create_job_for_testcase
from common.models import BlackListWord
from django.test import TestCase
from member.dtos.model_dtos import JobExperience
from member.models import (
    Member,
    MemberJobExperience,
)
from member.services import (
    add_member_job_experiences,
    check_email_exists,
    check_nickname_exists,
    check_nickname_valid,
    check_only_alphanumeric,
    check_only_korean_english_alphanumeric,
    check_username_exists,
)


class MemberCheckMemberInfoTestCase(TestCase):
    def setUp(self):
        pass

    def test_check_username_exists_should_return_true_when_username_exists(self):
        # Given: test 라는 이름을 가진 Member 생성
        Member.objects.create_user(username='test')

        # Expected:
        self.assertEqual(check_username_exists('test'), True)

    def test_check_username_exists_should_return_false_when_username_not_exists(self):
        # Expected:
        self.assertEqual(check_username_exists('test'), False)

    def test_check_nickname_exists_should_return_true_when_username_exists(self):
        # Given: test 라는 nickname 을 가진 Member 생성
        Member.objects.create_user(username='aaaa', nickname='test')

        # Expected:
        self.assertEqual(check_nickname_exists('test'), True)

    def test_check_nickname_exists_should_return_false_when_username_not_exists(self):
        # Expected:
        self.assertEqual(check_nickname_exists('test'), False)

    def test_check_email_exists_should_return_true_when_username_exists(self):
        # Given: test 라는 email 을 가진 Member 생성
        Member.objects.create_user(username='aaaa', email='test@naver.com')

        # Expected:
        self.assertEqual(check_email_exists('test@naver.com'), True)

    def test_check_email_exists_should_return_false_when_username_not_exists(self):
        # Expected:
        self.assertEqual(check_email_exists('test@naver.com'), False)

    def test_check_nickname_valid_when_valid(self):
        # Given: test 라는 nickname 을 가진 Member 생성
        # Expected:
        self.assertEqual(check_nickname_valid('test'), True)

    def test_check_nickname_valid_when_invalid(self):
        # Given: test 라는 nickname 을 가진 Member 생성
        BlackListWord.objects.create(
            black_list_section_id=1,
            wording='test',
        )

        # Expected:
        self.assertEqual(check_nickname_valid('123test'), False)


class CheckRegexTestCase(TestCase):
    def test_check_only_alphanumeric(self):
        self.assertEqual(check_only_alphanumeric("abc123"), True)
        self.assertEqual(check_only_alphanumeric("abc@123"), False)
        self.assertEqual(check_only_alphanumeric("한글123"), False)

    def test_check_only_korean_english_alphanumeric(self):
        self.assertEqual(check_only_korean_english_alphanumeric("안녕abc123"), True)
        self.assertEqual(check_only_korean_english_alphanumeric("안녕abc@123"), False)
        self.assertEqual(check_only_korean_english_alphanumeric("가나다ABC123"), True)


class AddMemberJobExperiencesTestCase(TestCase):
    def setUp(self):
        # Given: 테스트에 필요한 데이터 설정
        self.member = Member.objects.create_user(username='test')
        self.job1 = create_job_for_testcase(name='Job 1')
        self.job2 = create_job_for_testcase(name='Job 2')
        self.job_experiences = [
            JobExperience(
                job_id=self.job1.id,
                start_date=date(2022, 1, 1),
                end_date=date(2022, 12, 31),
            ),
            JobExperience(
                job_id=self.job2.id,
                start_date=date(2023, 1, 1),
                end_date=date(2023, 12, 31),
            )
        ]

    def test_add_member_job_experiences(self):
        # Given:
        # When: 함수 실행
        created_experiences = add_member_job_experiences(self.member.id, self.job_experiences)

        # Then: 결과 검증
        self.assertEqual(len(created_experiences), 2)
        self.assertEqual(MemberJobExperience.objects.count(), 2)

        for exp, created_exp in zip(self.job_experiences, created_experiences):
            self.assertEqual(created_exp.member_id, self.member.id)
            self.assertEqual(created_exp.job_id, exp.job_id)
            self.assertEqual(created_exp.start_date, exp.start_date)
            self.assertEqual(created_exp.end_date, exp.end_date)
            self.assertIsNotNone(created_exp.created_at)

    def test_add_member_job_experiences_empty_list(self):
        # Given: 빈 리스트로 테스트
        # When: 함수 실행
        created_experiences = add_member_job_experiences(self.member.id, [])

        # Then: 결과 검증
        self.assertEqual(len(created_experiences), 0)
        self.assertEqual(MemberJobExperience.objects.count(), 0)
