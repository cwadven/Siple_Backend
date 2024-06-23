from common.dtos.helper_dtos import ConstanceType
from job.models import JobCategory
from job.services.project_job_services import get_active_job_categories
from project.models import ProjectCategory
from project.services.project_services import get_active_project_categories


class ConstanceTypeHelper(object):
    def get_constance_types(self) -> list[ConstanceType]:
        raise NotImplementedError


class ConstanceJobCategoryTypeHelper(ConstanceTypeHelper):
    @staticmethod
    def get_job_categories() -> list[JobCategory]:
        return get_active_job_categories()

    def get_constance_types(self) -> list[ConstanceType]:
        return [
            ConstanceType(
                id=category.id,
                name=category.name,
                display_name=category.display_name,
            )
            for category in self.get_job_categories()
        ]


class ConstanceProjectCategoryTypeHelper(ConstanceTypeHelper):
    @staticmethod
    def get_project_categories() -> list[ProjectCategory]:
        return get_active_project_categories()

    def get_constance_types(self) -> list[ConstanceType]:
        return [
            ConstanceType(
                id=category.id,
                name=category.name,
                display_name=category.display_name,
            )
            for category in self.get_project_categories()
        ]


CONSTANCE_TYPE_HELPER_MAPPER = {
    'job-category': ConstanceJobCategoryTypeHelper(),
    'project-category': ConstanceProjectCategoryTypeHelper(),
}
