from datetime import date
from unittest.mock import patch

from common.common_testcase_helpers.job.testcase_helpers import create_job_for_testcase
from common.common_testcase_helpers.member.testcase_helpers import create_member_attribute_type_for_testcase
from common.models import BlackListWord
from django.test import TestCase
from member.dtos.model_dtos import (
    JobExperience,
    MemberInfoBlock,
    MemberJobExperienceDuration,
    MemberMainAttribute,
)
from member.models import (
    Member,
    MemberAttribute,
    MemberExtraLink,
    MemberInformation,
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
    get_active_member_extra_link_qa,
    get_active_member_information_qs,
    get_member_info_block,
    get_members_job_experience_durations,
    get_members_main_attributes_with_sort,
    get_members_project_ongoing_info,
)
from project.consts import (
    ProjectMemberManagementLeftStatus,
    ProjectResultStatus,
    ProjectStatus,
)
from project.dtos.model_dtos import ProjectOngoingInfo
from project.models import (
    Project,
    ProjectMemberManagement,
    ProjectRecruitApplication,
    ProjectRecruitment,
    ProjectRecruitmentJob,
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
        BlackListWord.objects.get_or_create(
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


class GetMembersProjectOngoingInfoTest(TestCase):
    def setUp(self):
        self.project_master = Member.objects.create_user(username='testm', nickname='testm')
        self.member1 = Member.objects.create_user(username='test1', nickname='test1')
        self.member2 = Member.objects.create_user(username='test2', nickname='test2')
        self.project = Project.objects.create(
            title='Project',
            created_member_id=self.project_master.id,
        )
        self.project_recruitment = ProjectRecruitment.objects.create(
            project=self.project,
            times_project_recruit=1,
            created_member_id=self.project_master.id,
        )
        self.job_backend = create_job_for_testcase('backend')
        self.project_recruitment_job = ProjectRecruitmentJob.objects.create(
            project_recruitment=self.project_recruitment,
            job=self.job_backend,
            total_limit=10,
            created_member_id=self.project_master.id,
        )
        self.project_recruit_application_member1 = ProjectRecruitApplication.objects.create(
            project_recruitment_job=self.project_recruitment_job,
            member_id=self.member1.id,
            request_message='Test',
        )
        self.project_recruit_application_member2 = ProjectRecruitApplication.objects.create(
            project_recruitment_job=self.project_recruitment_job,
            member_id=self.member2.id,
            request_message='Test',
        )
        self.project_member_management_member_master = ProjectMemberManagement.objects.create(
            project=self.project,
            member=self.project_master,
            project_recruit_application=None,
            job=None,
            left_status=None,
        )
        self.project_member_management_member1 = ProjectMemberManagement.objects.create(
            project=self.project,
            member=self.member1,
            project_recruit_application=self.project_recruit_application_member1,
            job=self.job_backend,
            left_status=None,
        )
        self.project_member_management_member2 = ProjectMemberManagement.objects.create(
            project=self.project,
            member=self.member2,
            project_recruit_application=self.project_recruit_application_member1,
            job=self.job_backend,
            left_status=None,
        )

    def test_get_members_project_ongoing_info_should_have_only_working(self):
        # Given: Set Working Project Status
        self.project.project_status = ProjectStatus.WORKING.value
        self.project.save()

        # When: get_members_project_ongoing_info
        result = get_members_project_ongoing_info([self.member1.id, self.member2.id, self.project_master.id])

        # Then: 결과 검증
        self.assertDictEqual(
            result,
            {
                self.member1.id: {'success': 0, 'working': 1, 'leaved': 0},
                self.member2.id: {'success': 0, 'working': 1, 'leaved': 0},
                self.project_master.id: {'success': 0, 'working': 1, 'leaved': 0},
            }
        )

    def test_get_members_project_ongoing_info_should_have_only_success(self):
        # Given: Set Working  ProjectResultStatus Success
        self.project.project_result_status = ProjectResultStatus.SUCCESS.value
        self.project.save()

        # When: get_members_project_ongoing_info
        result = get_members_project_ongoing_info([self.member1.id, self.member2.id, self.project_master.id])

        # Then: 결과 검증
        self.assertDictEqual(
            result,
            {
                self.member1.id: {'success': 1, 'working': 0, 'leaved': 0},
                self.member2.id: {'success': 1, 'working': 0, 'leaved': 0},
                self.project_master.id: {'success': 1, 'working': 0, 'leaved': 0},
            }
        )

    def test_get_members_project_ongoing_info_should_have_left(self):
        # Given: Set Working  ProjectResultStatus Success
        self.project.project_result_status = ProjectResultStatus.SUCCESS.value
        self.project.save()
        # And: Set left
        self.project_member_management_member1.left_status = ProjectMemberManagementLeftStatus.LEFT.value
        self.project_member_management_member1.save()

        # When: get_members_project_ongoing_info
        result = get_members_project_ongoing_info([self.member1.id, self.member2.id, self.project_master.id])

        # Then: 결과 검증
        self.assertDictEqual(
            result,
            {
                self.member1.id: {'success': 0, 'working': 0, 'leaved': 1},
                self.member2.id: {'success': 1, 'working': 0, 'leaved': 0},
                self.project_master.id: {'success': 1, 'working': 0, 'leaved': 0},
            }
        )


class GetMembersMainAttributesWithSortTest(TestCase):
    def setUp(self):
        self.member1 = Member.objects.create_user(username='test1', nickname='test1')
        self.member2 = Member.objects.create_user(username='test2', nickname='test2')
        self.member_attribute_type_kind = create_member_attribute_type_for_testcase('kind')
        self.member_attribute_type_help = create_member_attribute_type_for_testcase('help')

    def test_get_members_main_attributes_with_sort(self):
        # Given: Set MemberAttribute
        MemberAttribute.objects.create(
            member=self.member1,
            member_attribute_type=self.member_attribute_type_kind,
            value=1,
        )
        MemberAttribute.objects.create(
            member=self.member1,
            member_attribute_type=self.member_attribute_type_help,
            value=2,
        )
        MemberAttribute.objects.create(
            member=self.member2,
            member_attribute_type=self.member_attribute_type_kind,
            value=2,
        )
        MemberAttribute.objects.create(
            member=self.member2,
            member_attribute_type=self.member_attribute_type_help,
            value=1,
        )

        # When: get_members_main_attributes_with_sort
        result = get_members_main_attributes_with_sort([self.member1.id, self.member2.id])

        # Then: 결과 검증
        self.assertDictEqual(
            result,
            {
                self.member1.id: [
                    {
                        'member_attribute_type_id': self.member_attribute_type_help.id,
                        'display_name': 'help',
                        'value': 2,
                    },
                    {
                        'member_attribute_type_id': self.member_attribute_type_kind.id,
                        'display_name': 'kind',
                        'value': 1,
                    },
                ],
                self.member2.id: [
                    {
                        'member_attribute_type_id': self.member_attribute_type_kind.id,
                        'display_name': 'kind',
                        'value': 2,
                    },
                    {
                        'member_attribute_type_id': self.member_attribute_type_help.id,
                        'display_name': 'help',
                        'value': 1,
                    },
                ],
            }
        )


class GetMembersJobExperienceDurationsTestCase(TestCase):

    def setUp(self):
        self.member1 = Member.objects.create_user(username='test1', nickname='test1')
        self.member2 = Member.objects.create_user(username='test2', nickname='test2')
        self.job1 = create_job_for_testcase('Developer')
        self.job2 = create_job_for_testcase('Designer')
        MemberJobExperience.objects.create(
            member=self.member1,
            job=self.job1,
            start_date=date(2020, 1, 1),
            end_date=date(2021, 1, 1),
        )
        MemberJobExperience.objects.create(
            member=self.member1,
            job=self.job1,
            start_date=date(2021, 2, 1),
            end_date=date(2022, 1, 1),
        )
        MemberJobExperience.objects.create(
            member=self.member2,
            job=self.job1,
            start_date=date(2020, 1, 1),
            end_date=date(2023, 1, 1),
        )
        MemberJobExperience.objects.create(
            member=self.member2,
            job=self.job2,
            start_date=date(2020, 1, 1),
            end_date=date(2023, 1, 1),
        )

    def test_get_members_job_experience_durations(self):
        # Given:
        member_ids = [self.member1.id, self.member2.id]
        expected_result = {
            self.member1.id: [
                {'job_id': self.job1.id, 'display_name': self.job1.display_name, 'total_year': 1, 'total_month': 11},
            ],
            self.member2.id: [
                {'job_id': self.job1.id, 'display_name': self.job1.display_name, 'total_year': 3, 'total_month': 0},
                {'job_id': self.job2.id, 'display_name': self.job2.display_name, 'total_year': 3, 'total_month': 0},
            ]
        }

        # When:
        result = get_members_job_experience_durations(member_ids)

        # Then:
        self.assertDictEqual(
            result,
            expected_result,
        )


class GetActiveMemberInformationQuerySetTestCase(TestCase):

    def setUp(self):
        self.member1 = Member.objects.create_user(username='test1', nickname='test1')
        self.member_information1 = MemberInformation.objects.create(
            member=self.member1,
            description='test1',
        )
        self.member_information2 = MemberInformation.objects.create(
            member=self.member1,
            description='test2',
        )

    @patch('member.services.MemberInformation.objects.filter')
    def test_get_active_member_information_qs(self,
                                              mock_filter):
        # Given:
        # When:
        get_active_member_information_qs(self.member1.id)

        # Then: Assert that MemberInformation.objects.filter is called with the correct data
        mock_filter.assert_called_once_with(
            member_id=self.member1.id, is_deleted=False
        )


class GetActiveMemberExtraLinkQuerySetTestCase(TestCase):
    def setUp(self):
        self.member1 = Member.objects.create_user(username='test1', nickname='test1')
        self.member_extra_link1 = MemberExtraLink.objects.create(
            member=self.member1,
            description='test1',
        )
        self.member_extra_link2 = MemberExtraLink.objects.create(
            member=self.member1,
            description='test2',
        )

    @patch('member.services.MemberExtraLink.objects.filter')
    def test_get_active_member_extra_link_qa(self,
                                             mock_filter):
        # Given:
        # When:
        get_active_member_extra_link_qa(self.member1.id)

        # Then: Assert that MemberInformation.objects.filter is called with the correct data
        mock_filter.assert_called_once_with(
            member_id=self.member1.id, is_deleted=False
        )


class GetMemberInfoBlockTestCase(TestCase):
    def setUp(self):
        self.member1 = Member.objects.create_user(
            username='test1',
            nickname='test1',
            profile_image_url='test1.jpg',
        )
        self.member_information1 = MemberInformation.objects.create(
            member=self.member1,
            description='test1',
        )
        self.member_information2 = MemberInformation.objects.create(
            member=self.member1,
            description='test2',
        )
        self.member_extra_link1 = MemberExtraLink.objects.create(
            member=self.member1,
            description='test1',
            sequence=1,
        )
        self.member_extra_link2 = MemberExtraLink.objects.create(
            member=self.member1,
            description='test2',
            sequence=2,
        )
        self.member_attribute_type_kind = create_member_attribute_type_for_testcase('kind')
        self.member_attribute_type_help = create_member_attribute_type_for_testcase('help')
        self.member_attribute1 = MemberAttribute.objects.create(
            member=self.member1,
            member_attribute_type=self.member_attribute_type_kind,
            value=4,
        )
        self.member_attribute2 = MemberAttribute.objects.create(
            member=self.member1,
            member_attribute_type=self.member_attribute_type_help,
            value=2,
        )
        self.job1 = create_job_for_testcase('Developer')
        MemberJobExperience.objects.create(
            member=self.member1,
            job=self.job1,
            start_date=date(2020, 1, 1),
            end_date=date(2021, 1, 1),
        )
        MemberJobExperience.objects.create(
            member=self.member1,
            job=self.job1,
            start_date=date(2021, 2, 1),
            end_date=date(2022, 1, 1),
        )
        self.project = Project.objects.create(
            title='Project',
            created_member_id=self.member1.id,
            project_result_status=ProjectResultStatus.SUCCESS.value,
            project_status=ProjectStatus.FINISHED.value,
        )
        self.project_member_management_member_master = ProjectMemberManagement.objects.create(
            project=self.project,
            member=self.member1,
            project_recruit_application=None,
            job=None,
            left_status=None,
        )

    @patch('member.services.get_members_project_ongoing_info')
    @patch('member.services.get_members_job_experience_durations')
    @patch('member.services.get_members_main_attributes_with_sort')
    @patch('member.services.get_active_member_extra_link_qa')
    @patch('member.services.get_active_member_information_qs')
    def test_get_member_info_block(self,
                                   mock_get_active_member_information_qs,
                                   mock_get_active_member_extra_link_qa,
                                   mock_get_members_main_attributes_with_sort,
                                   mock_get_members_job_experience_durations,
                                   mock_get_members_project_ongoing_info):
        # Given: Mocking
        mock_get_active_member_information_qs.return_value = MemberInformation.objects.filter(
            member_id=self.member1.id,
            is_deleted=False,
        )
        mock_get_active_member_extra_link_qa.return_value = MemberExtraLink.objects.filter(
            member_id=self.member1.id,
            is_deleted=False,
        )
        mock_get_members_main_attributes_with_sort.return_value = {
            self.member1.id: [
                {
                    'member_attribute_type_id': self.member_attribute_type_kind.id,
                    'display_name': self.member_attribute_type_kind.display_name,
                    'value': 4,
                },
                {
                    'member_attribute_type_id': self.member_attribute_type_help.id,
                    'display_name': self.member_attribute_type_help.display_name,
                    'value': 2,
                },
            ]
        }
        mock_get_members_job_experience_durations.return_value = {
            self.member1.id: [
                {'job_id': self.job1.id, 'display_name': self.job1.display_name, 'total_year': 1, 'total_month': 11},
            ]
        }
        mock_get_members_project_ongoing_info.return_value = {
            self.member1.id: {'success': 1, 'working': 0, 'leaved': 0},
        }

        # When:
        member_info_block = get_member_info_block(self.member1.id)

        # Then: Instance Check
        self.assertIsInstance(member_info_block, MemberInfoBlock)
        # And: Attribute Check
        self.assertEqual(member_info_block.member_id, self.member1.id)
        self.assertEqual(member_info_block.profile_image, self.member1.profile_image_url)
        self.assertEqual(member_info_block.nickname, self.member1.nickname)
        self.assertEqual(
            member_info_block.simple_description,
            self.member_information2.description,
        )
        self.assertEqual(member_info_block.link, self.member_extra_link1.url)
        self.assertEqual(
            member_info_block.project_info,
            ProjectOngoingInfo(success=1, working=0, leaved=0),
        )
        self.assertEqual(
            member_info_block.member_main_attributes,
            [
                MemberMainAttribute(
                    member_attribute_type_id=self.member_attribute_type_kind.id,
                    display_name=self.member_attribute_type_kind.display_name,
                ),
                MemberMainAttribute(
                    member_attribute_type_id=self.member_attribute_type_help.id,
                    display_name=self.member_attribute_type_help.display_name,
                ),
            ],
        )
        self.assertEqual(
            member_info_block.member_job_experiences,
            [
                MemberJobExperienceDuration(
                    job_id=self.job1.id,
                    display_name=self.job1.display_name,
                    total_year=1,
                    total_month=11,
                )
            ],
        )
        # And: Mocking Check
        mock_get_active_member_information_qs.assert_called_once_with(member_id=self.member1.id)
        mock_get_active_member_extra_link_qa.assert_called_once_with(member_id=self.member1.id)
        mock_get_members_main_attributes_with_sort.assert_called_once_with([self.member1.id])
        mock_get_members_job_experience_durations.assert_called_once_with([self.member1.id])
        mock_get_members_project_ongoing_info.assert_called_once_with([self.member1.id])

    def test_get_member_info_block_when_member_information_is_none(self):
        # Given: Mocking as Member Information is None
        self.member_information1.is_deleted = True
        self.member_information1.save()
        self.member_information2.is_deleted = True
        self.member_information2.save()

        # When:
        member_info_block = get_member_info_block(self.member1.id)

        # Then: Instance Check
        self.assertIsInstance(member_info_block, MemberInfoBlock)
        # And: Attribute Check
        self.assertEqual(
            member_info_block.simple_description,
            None,
        )

    def test_get_member_info_block_when_member_extra_link_is_none(self):
        # Given: Mocking as Member Extra Link is None
        self.member_extra_link1.is_deleted = True
        self.member_extra_link1.save()
        self.member_extra_link2.is_deleted = True
        self.member_extra_link2.save()
        # When:
        member_info_block = get_member_info_block(self.member1.id)

        # Then: Instance Check
        self.assertIsInstance(member_info_block, MemberInfoBlock)
        # And: Attribute Check
        self.assertEqual(
            member_info_block.link,
            None,
        )

    def test_get_member_info_block_when_members_main_attributes_not_exists(self):
        # Given: Mocking as Member Attribute Not Exists
        MemberAttribute.objects.all().delete()

        # When:
        member_info_block = get_member_info_block(self.member1.id)

        # Then: Instance Check
        self.assertIsInstance(member_info_block, MemberInfoBlock)
        # And: Attribute Check
        self.assertEqual(
            member_info_block.member_main_attributes,
            None,
        )

    def test_get_member_info_block_when_member_job_experiences_not_exists(self):
        # Given: Mocking as MemberJobExperience Not Exists
        MemberJobExperience.objects.all().delete()

        # When:
        member_info_block = get_member_info_block(self.member1.id)

        # Then: Instance Check
        self.assertIsInstance(member_info_block, MemberInfoBlock)
        # And: Attribute Check
        self.assertEqual(
            member_info_block.member_job_experiences,
            None,
        )
