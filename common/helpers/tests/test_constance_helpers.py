from unittest.mock import patch

from common.common_testcase_helpers.job.testcase_helpers import (
    create_job_category_for_testcase,
    create_job_for_testcase,
)
from common.common_testcase_helpers.project.testcase_helpers import create_project_category_for_testcase
from common.dtos.helper_dtos import (
    ConstanceDetailType,
    ConstanceIconImageType,
    ConstanceType,
)
from common.helpers.constance_helpers import (
    CONSTANCE_TYPE_HELPER_MAPPER,
    ConstanceDetailTypeHelper,
    ConstanceIconImageTypeHelper,
    ConstanceJobCategoryTypeHelper,
    ConstanceJobDetailTypeHelper,
    ConstanceProjectCategoryIconImageTypeHelper,
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


class ConstanceIconImageTypeHelperTest(TestCase):
    def test_get_constance_icon_image_types(self):
        # Given: Set up the test data
        # Expected: Assert the result
        with self.assertRaises(NotImplementedError):
            ConstanceIconImageTypeHelper().get_constance_icon_image_types()


class ConstanceDetailTypeHelperTest(TestCase):
    def test_constance_detail_type_helper(self):
        # Given: Set up the test data
        # Expected: Assert the result
        with self.assertRaises(NotImplementedError):
            ConstanceDetailTypeHelper().get_constance_detail_types()


class ConstanceProjectCategoryIconImageTypeHelperTest(TestCase):
    def setUp(self):
        self.project_category1 = create_project_category_for_testcase('project_category1')
        self.project_category2 = create_project_category_for_testcase('project_category2')

    @patch('common.helpers.constance_helpers.get_active_project_categories')
    def test_get_project_categories(self, mock_get_active_project_categories):
        # Given: Set up the test data
        mock_get_active_project_categories.return_value = [self.project_category1, self.project_category2]

        # When: Call the function
        project_categories = ConstanceProjectCategoryIconImageTypeHelper().get_project_categories()

        # Then: Assert the result
        self.assertEqual(project_categories, [self.project_category1, self.project_category2])
        mock_get_active_project_categories.assert_called_once()

    @patch('common.helpers.constance_helpers.ConstanceProjectCategoryIconImageTypeHelper.get_project_categories')
    def test_get_constance_icon_image_types(self, mock_get_project_categories):
        # Given: Set up the test data
        self.project_category1.icon_image = 'icon_image1'
        self.project_category1.save()
        self.project_category2.icon_image = 'icon_image2'
        self.project_category2.save()
        mock_get_project_categories.return_value = [self.project_category1, self.project_category2]

        # When: Call the function
        constance_types = ConstanceProjectCategoryIconImageTypeHelper().get_constance_icon_image_types()

        # Then: Assert the result
        self.assertEqual(
            constance_types,
            [
                ConstanceIconImageType(
                    id=self.project_category1.id,
                    name=self.project_category1.name,
                    display_name=self.project_category1.display_name,
                    icon_image='icon_image1',
                ),
                ConstanceIconImageType(
                    id=self.project_category2.id,
                    name=self.project_category2.name,
                    display_name=self.project_category2.display_name,
                    icon_image='icon_image2',
                ),
            ],
        )
        mock_get_project_categories.assert_called_once()


class ConstanceJobDetailTypeHelperTest(TestCase):
    def setUp(self):
        self.job_category1 = create_job_category_for_testcase('job_category1')
        self.job_category2 = create_job_category_for_testcase('job_category2')
        self.backend = create_job_for_testcase('backend')
        self.backend.category = self.job_category1
        self.backend.save()
        self.frontend = create_job_for_testcase('frontend')
        self.frontend.category = self.job_category2
        self.frontend.save()
        self.none_job = create_job_for_testcase('none_job')

    @patch('common.helpers.constance_helpers.get_active_jobs')
    def test_get_jobs(self, mock_get_active_jobs):
        # Given: Set up the test data
        mock_get_active_jobs.return_value = [self.backend, self.frontend, self.none_job]

        # When: Call the function
        jobs = ConstanceJobDetailTypeHelper().get_jobs()

        # Then: Assert the result
        self.assertEqual(jobs, [self.backend, self.frontend, self.none_job])
        mock_get_active_jobs.assert_called_once()

    def test_get_constance_detail_types(self):
        # Given: Set up the test data
        # When: Call the function
        constance_types = ConstanceJobDetailTypeHelper().get_constance_detail_types()

        # Then: Assert the result
        self.assertEqual(
            constance_types,
            [
                ConstanceDetailType(
                    id=self.backend.id,
                    name=self.backend.name,
                    display_name=self.backend.display_name,
                    parent_id=self.backend.category.id,
                    parent_name=self.backend.category.name,
                    parent_display_name=self.backend.category.display_name,
                ),
                ConstanceDetailType(
                    id=self.frontend.id,
                    name=self.frontend.name,
                    display_name=self.frontend.display_name,
                    parent_id=self.frontend.category.id,
                    parent_name=self.frontend.category.name,
                    parent_display_name=self.frontend.category.display_name,
                ),
                ConstanceDetailType(
                    id=self.none_job.id,
                    name=self.none_job.name,
                    display_name=self.none_job.display_name,
                    parent_id=None,
                    parent_name=None,
                    parent_display_name=None,
                ),
            ],
        )
