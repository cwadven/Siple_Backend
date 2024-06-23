from common.common_consts.common_error_messages import ErrorMessage
from django.http import QueryDict
from django.test import TestCase
from project.consts import (
    ProjectCurrentRecruitStatus,
    ProjectJobExperienceType,
    ProjectJobSearchOperator,
)
from project.dtos.request_dtos import (
    CreateProjectRequest,
    HomeProjectListRequest,
)
from pydantic import ValidationError


class HomeProjectListRequestTest(TestCase):
    def test_check_if_integer_valid(self):
        # Given: valid category_ids and job_ids
        valid_category_ids = [1, '2', 3]
        valid_job_ids = ['4', 5, '6']
        valid_job_category_ids = ['4', 5, '6']

        # When: check_if_integer 함수 실행
        category_ids_result = HomeProjectListRequest.check_if_integer(valid_category_ids)
        job_ids_result = HomeProjectListRequest.check_if_integer(valid_job_ids)
        job_category_ids_result = HomeProjectListRequest.check_if_integer(valid_job_category_ids)

        # Then: 정수로 변환된 리스트 반환
        self.assertEqual(category_ids_result, [1, 2, 3])
        self.assertEqual(job_ids_result, [4, 5, 6])
        self.assertEqual(job_category_ids_result, [4, 5, 6])

    def test_check_if_integer_invalid(self):
        # Given: invalid category_ids
        invalid_category_ids = ['a', 2.5, '3.0']

        # When/Then: ValueError 발생
        with self.assertRaises(ValueError) as context:
            HomeProjectListRequest.check_if_integer(invalid_category_ids)
        self.assertEqual(str(context.exception), ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)

    def test_check_if_integer_invalid_list(self):
        # Given: invalid category_ids type not as list
        invalid_category_ids = '111'

        # When/Then: ValueError 발생
        with self.assertRaises(ValueError) as context:
            HomeProjectListRequest.check_if_integer(invalid_category_ids)
        self.assertEqual(str(context.exception), ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)

    def test_check_if_none_or_integer_valid(self):
        # Given: valid min_hours_per_week and max_hours_per_week
        valid_min_hours_per_week = 10
        valid_max_hours_per_week = None

        # When: check_if_none_or_integer 함수 실행
        min_hours_result = HomeProjectListRequest.check_if_none_or_integer(valid_min_hours_per_week)
        max_hours_result = HomeProjectListRequest.check_if_none_or_integer(valid_max_hours_per_week)

        # Then: 정수 반환
        self.assertEqual(min_hours_result, 10)
        self.assertIsNone(max_hours_result)

    def test_check_if_none_or_integer_invalid(self):
        # Given: invalid min_hours_per_week
        invalid_min_hours_per_week = 'ten'

        # When/Then: ValueError 발생
        with self.assertRaises(ValueError) as context:
            HomeProjectListRequest.check_if_none_or_integer(invalid_min_hours_per_week)
        self.assertEqual(str(context.exception), ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)

    def test_check_jobs_operator_value_valid(self):
        # Given: valid jobs_operator
        valid_jobs_operator = 'OR'

        # When: check_jobs_operator_value 함수 실행
        jobs_operator_result = HomeProjectListRequest.check_jobs_operator_value(valid_jobs_operator)

        # Then: OR 반환
        self.assertEqual(jobs_operator_result, ProjectJobSearchOperator.OR.value)

    def test_check_jobs_operator_value_as_none(self):
        # Given: valid jobs_operator as None
        valid_jobs_operator = None

        # When: check_jobs_operator_value 함수 실행
        jobs_operator_result = HomeProjectListRequest.check_jobs_operator_value(valid_jobs_operator)

        # Then: OR 반환
        self.assertEqual(jobs_operator_result, ProjectJobSearchOperator.OR.value)

    def test_check_jobs_operator_value_invalid(self):
        # Given: invalid jobs_operator
        invalid_jobs_operator = 'INVALID_OPERATOR'

        # When/Then: ValueError 발생
        with self.assertRaises(ValueError) as context:
            HomeProjectListRequest.check_jobs_operator_value(invalid_jobs_operator)
        self.assertEqual(str(context.exception), ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)

    def test_check_experience_value_valid(self):
        # Given: valid experience
        valid_experience = 'ALL'

        # When: check_experience_value 함수 실행
        experience_result = HomeProjectListRequest.check_experience_value(valid_experience)

        # Then: ALL 반환
        self.assertEqual(experience_result, ProjectJobExperienceType.ALL.value)

    def test_check_experience_value_as_none(self):
        # Given: valid experience
        valid_experience = None

        # When: check_experience_value 함수 실행
        experience_result = HomeProjectListRequest.check_experience_value(valid_experience)

        # Then: ALL 반환
        self.assertEqual(experience_result, None)

    def test_check_experience_value_invalid(self):
        # Given: invalid experience
        invalid_experience = 'INVALID_EXPERIENCE'

        # When/Then: ValueError 발생
        with self.assertRaises(ValueError) as context:
            HomeProjectListRequest.check_experience_value(invalid_experience)
        self.assertEqual(str(context.exception), ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)

    def test_validate_min_and_max_hours_per_week_valid(self):
        # Given: Valid input data
        data = {
            'title': 'Test Project',
            'min_hours_per_week': 10,
            'max_hours_per_week': 20
        }

        # When: Creating HomeProjectListRequest instance
        instance = HomeProjectListRequest(**data)

        # Then: No validation errors should be raised
        self.assertEqual(instance.min_hours_per_week, 10)
        self.assertEqual(instance.max_hours_per_week, 20)

    def test_validate_min_and_max_hours_per_week_invalid(self):
        # Given: Invalid input data where min_hours_per_week is greater than max_hours_per_week
        data = {
            'title': 'Test Project',
            'min_hours_per_week': 20,
            'max_hours_per_week': 10
        }

        # When: Expecting a ValidationError to be raised
        with self.assertRaises(ValidationError) as context:
            HomeProjectListRequest(**data)

        # Then: Validate the error details
        errors = context.exception.errors()
        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[0]['loc'], ('min_hours_per_week',))
        self.assertEqual(
            errors[0]['msg'].split(',')[1].strip(),
            'min_hours_per_week 값은 max_hours_per_week 보다 작아야합니다.',
        )
        self.assertEqual(errors[0]['type'], ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_SMALLER.value)
        self.assertEqual(errors[1]['loc'], ('max_hours_per_week',))
        self.assertEqual(
            errors[1]['msg'].split(',')[1].strip(),
            'max_hours_per_week 값은 min_hours_per_week 보다 커야합니다.',
        )
        self.assertEqual(errors[1]['type'], ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_BIGGER.value)

    def test_validate_job_ids_maximum_input_length_valid(self):
        # Given: Valid input data
        data = {
            'title': 'Test Project',
            'job_ids': [1, 2, 3, 4, 5]
        }

        # When: Creating HomeProjectListRequest instance
        instance = HomeProjectListRequest(**data)

        # Then: No validation errors should be raised
        self.assertEqual(instance.job_ids, [1, 2, 3, 4, 5])

    def test_validate_job_ids_maximum_input_length_invalid(self):
        # Given: Invalid input data where job_ids length is greater than 5
        data = {
            'title': 'Test Project',
            'job_ids': [1, 2, 3, 4, 5, 6]
        }

        # When: Expecting a ValidationError to be raised
        with self.assertRaises(ValidationError) as context:
            HomeProjectListRequest(**data)

        # Then: Validate the error details
        errors = context.exception.errors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['loc'], ('job_ids',))
        self.assertEqual(errors[0]['msg'].split(',')[1].strip(), ErrorMessage.INVALID_MAXIMUM_LENGTH.label)
        self.assertEqual(errors[0]['type'], ErrorMessage.INVALID_MAXIMUM_LENGTH.value)

    def test_validate_min_and_max_duration_month_valid(self):
        # Given: Valid input data
        data = {
            'title': 'Test Project',
            'min_duration_month': 10,
            'max_duration_month': 20
        }

        # When: Creating HomeProjectListRequest instance
        instance = HomeProjectListRequest(**data)

        # Then: No validation errors should be raised
        self.assertEqual(instance.min_duration_month, 10)
        self.assertEqual(instance.max_duration_month, 20)

    def test_validate_min_and_max_duration_month_invalid(self):
        # Given: Invalid input data where min_duration_month is greater than max_duration_month
        data = {
            'title': 'Test Project',
            'min_duration_month': 20,
            'max_duration_month': 10
        }

        # When: Expecting a ValidationError to be raised
        with self.assertRaises(ValidationError) as context:
            HomeProjectListRequest(**data)

        # Then: Validate the error details
        errors = context.exception.errors()
        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[0]['loc'], ('min_duration_month',))
        self.assertEqual(
            errors[0]['msg'].split(',')[1].strip(),
            'min_duration_month 값은 max_duration_month 보다 작아야합니다.',
        )
        self.assertEqual(errors[0]['type'], ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_SMALLER.value)
        self.assertEqual(errors[1]['loc'], ('max_duration_month',))
        self.assertEqual(
            errors[1]['msg'].split(',')[1].strip(),
            'max_duration_month 값은 min_duration_month 보다 커야합니다.',
        )
        self.assertEqual(errors[1]['type'], ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_BIGGER.value)

    def test_of_method(self):
        # Given: request_data
        request_data = QueryDict(mutable=True)
        request_data.update({
            'title': 'Project Title',
            'category_ids': '1,2,3',
            'job_ids': '4,5,6',
            'jobs_operator': ProjectJobSearchOperator.OR.value,
            'experience': ProjectJobExperienceType.ALL.value,
            'min_hours_per_week': 10,
            'max_hours_per_week': 20,
            'min_duration_month': 6,
            'max_duration_month': 12,
            'current_recruit_status': ProjectCurrentRecruitStatus.RECRUITING.value,
        })

        # When: of 함수 실행
        result = HomeProjectListRequest.of(request_data)

        # Then: HomeProjectListRequest 객체 반환
        self.assertEqual(result.title, 'Project Title')
        self.assertEqual(result.category_ids, [1, 2, 3])
        self.assertEqual(result.job_ids, [4, 5, 6])
        self.assertEqual(result.jobs_operator, ProjectJobSearchOperator.OR.value)
        self.assertEqual(result.experience, ProjectJobExperienceType.ALL.value)
        self.assertEqual(result.min_hours_per_week, 10)
        self.assertEqual(result.max_hours_per_week, 20)
        self.assertEqual(result.min_duration_month, 6)
        self.assertEqual(result.max_duration_month, 12)
        self.assertEqual(result.current_recruit_status, ProjectCurrentRecruitStatus.RECRUITING.value)


class CreateProjectRequestTest(TestCase):
    def setUp(self):
        self.payload = {
            'title': 'Project Title',
            'description': 'Project Description',
            'category_id': 1,
            'hours_per_week': 10,
            'duration_month': 3,
            'experience': ProjectJobExperienceType.ALL.value,
            'extra_information': 'Extra Information',
            'image': 'Image URL',
            'jobs': [
                {
                    'job_id': 1,
                    'total_limit': 5,
                },
                {
                    'job_id': 2,
                    'total_limit': 10,
                },
            ],
        }

    def test_check_experience_value_should_raise_error_when_invalid_type(self):
        # Given:
        self.payload['experience'] = 'INVALID_TYPE'

        # When: Expecting a ValidationError to be raised
        with self.assertRaises(ValidationError) as context:
            CreateProjectRequest.of(self.payload)

        # Then: Validate the error details
        errors = context.exception.errors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['loc'], ('experience',))
        self.assertEqual(
            errors[0]['msg'].split(',')[1].strip(),
            ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label,
        )

    def test_check_jobs_value_should_raise_error_when_invalid_length(self):
        # Given: jobs length is 0
        self.payload['jobs'] = []

        # When: Expecting a ValidationError to be raised
        with self.assertRaises(ValidationError) as context:
            CreateProjectRequest.of(self.payload)

        # Then: Validate the error details
        errors = context.exception.errors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['loc'], ('jobs',))
        self.assertEqual(
            errors[0]['msg'].split(',')[1].strip(),
            ErrorMessage.INVALID_MINIMUM_ITEM_SIZE.label.format(1),
        )

    def test_check_jobs_value_should_raise_error_when_invalid_values(self):
        # Given: jobs invalid keys
        self.payload['jobs'] = [
            {'invalid': 10},
            {'invalid': 10},
        ]

        # When: Expecting a ValidationError to be raised
        with self.assertRaises(ValidationError) as context:
            CreateProjectRequest.of(self.payload)

        # Then: Validate the error details
        errors = context.exception.errors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['loc'], ('jobs',))
        self.assertEqual(
            errors[0]['msg'].split(',')[1].strip(),
            ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label,
        )
