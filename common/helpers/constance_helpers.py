from common.dtos.helper_dtos import (
    ConstanceDetailType,
    ConstanceIconImageType,
    ConstanceType,
)
from job.models import (
    Job,
    JobCategory,
)
from job.services.project_job_services import (
    get_active_job_categories,
    get_active_jobs,
)
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
}


class ConstanceIconImageTypeHelper(object):
    def get_constance_icon_image_types(self) -> list[ConstanceIconImageType]:
        raise NotImplementedError


class ConstanceProjectCategoryIconImageTypeHelper(ConstanceIconImageTypeHelper):
    @staticmethod
    def get_project_categories() -> list[ProjectCategory]:
        return get_active_project_categories()

    def get_constance_icon_image_types(self) -> list[ConstanceIconImageType]:
        return [
            ConstanceIconImageType(
                id=category.id,
                name=category.name,
                display_name=category.display_name,
                icon_image=category.icon_image,
            )
            for category in self.get_project_categories()
        ]


class ConstanceDetailTypeHelper(object):
    def get_constance_detail_types(self) -> list[ConstanceDetailType]:
        raise NotImplementedError


class ConstanceJobDetailTypeHelper(ConstanceDetailTypeHelper):
    @staticmethod
    def get_jobs() -> list[Job]:
        return get_active_jobs()

    def get_constance_detail_types(self) -> list[ConstanceDetailType]:
        return [
            ConstanceDetailType(
                id=job.id,
                name=job.name,
                display_name=job.display_name,
                parent_id=job.category_id,
                parent_name=getattr(job.category, 'name', None),
                parent_display_name=getattr(job.category, 'display_name', None),
            )
            for job in self.get_jobs()
        ]
