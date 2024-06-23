from unittest.mock import patch

from common.common_testcase_helpers.job.testcase_helpers import create_job_category_for_testcase
from common.common_testcase_helpers.project.testcase_helpers import create_project_category_for_testcase
from common.dtos.helper_dtos import ConstanceType
from common.helpers.constance_helpers import (
    CONSTANCE_TYPE_HELPER_MAPPER,
    ConstanceJobCategoryTypeHelper,
    ConstanceProjectCategoryTypeHelper,
    ConstanceTypeHelper,
)
from django.test import TestCase


class ConstanceTypeHelperTest(TestCase):
    def test_constance_type_helper(self):
        # Given: Set up the test data
        # Expected: Assert the result
        with self.assertRaises(NotImplementedError):
            ConstanceTypeHelper().get_constance_types()


class ConstanceJobCategoryTypeHelperTest(TestCase):
    def setUp(self):
        self.job_category1 = create_job_category_for_testcase('job_category1')
        self.job_category2 = create_job_category_for_testcase('job_category2')

    @patch('common.helpers.constance_helpers.get_active_job_categories')
    def test_get_job_categories(self, mock_get_active_job_categories):
        # Given: Set up the test data
        mock_get_active_job_categories.return_value = [self.job_category1, self.job_category2]

        # When: Call the function
        job_categories = ConstanceJobCategoryTypeHelper().get_job_categories()

        # Then: Assert the result
        self.assertEqual(job_categories, [self.job_category1, self.job_category2])
        mock_get_active_job_categories.assert_called_once()

    @patch('common.helpers.constance_helpers.ConstanceJobCategoryTypeHelper.get_job_categories')
    def test_get_constance_types(self, mock_get_job_categories):
        # Given: Set up the test data
        mock_get_job_categories.return_value = [self.job_category1, self.job_category2]

        # When: Call the function
        constance_types = ConstanceJobCategoryTypeHelper().get_constance_types()

        # Then: Assert the result
        self.assertEqual(
            constance_types,
            [
                ConstanceType(id=self.job_category1.id, name=self.job_category1.name, display_name=self.job_category1.display_name),
                ConstanceType(id=self.job_category2.id, name=self.job_category2.name, display_name=self.job_category2.display_name),
            ],
        )
        mock_get_job_categories.assert_called_once()


class ConstanceProjectCategoryTypeHelperTest(TestCase):
    def setUp(self):
        self.project_category1 = create_project_category_for_testcase('project_category1')
        self.project_category2 = create_project_category_for_testcase('project_category2')

    @patch('common.helpers.constance_helpers.get_active_project_categories')
    def test_get_project_categories(self, mock_get_active_project_categories):
        # Given: Set up the test data
        mock_get_active_project_categories.return_value = [self.project_category1, self.project_category2]

        # When: Call the function
        project_categories = ConstanceProjectCategoryTypeHelper().get_project_categories()

        # Then: Assert the result
        self.assertEqual(project_categories, [self.project_category1, self.project_category2])
        mock_get_active_project_categories.assert_called_once()

    @patch('common.helpers.constance_helpers.ConstanceProjectCategoryTypeHelper.get_project_categories')
    def test_get_constance_types(self, mock_get_project_categories):
        # Given: Set up the test data
        mock_get_project_categories.return_value = [self.project_category1, self.project_category2]

        # When: Call the function
        constance_types = ConstanceProjectCategoryTypeHelper().get_constance_types()

        # Then: Assert the result
        self.assertEqual(
            constance_types,
            [
                ConstanceType(id=self.project_category1.id, name=self.project_category1.name, display_name=self.project_category1.display_name),
                ConstanceType(id=self.project_category2.id, name=self.project_category2.name, display_name=self.project_category2.display_name),
            ],
        )
        mock_get_project_categories.assert_called_once()


class ConstanceTypeMapperTest(TestCase):
    def test_constance_type_mapper_job_category(self):
        # Given:
        # When: Call
        constance_type_helper = CONSTANCE_TYPE_HELPER_MAPPER['job-category']

        # Then: Assert the result
        self.assertIsInstance(constance_type_helper, ConstanceJobCategoryTypeHelper)

    def test_constance_type_mapper_project_category(self):
        # Given:
        # When: Call
        constance_type_helper = CONSTANCE_TYPE_HELPER_MAPPER['project-category']

        # Then: Assert the result
        self.assertIsInstance(constance_type_helper, ConstanceProjectCategoryTypeHelper)
