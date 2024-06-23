from job.models import Job, JobCategory


def create_job_for_testcase(name: str) -> Job:
    return Job.objects.create(
        display_name=name,
        name=name,
        description=name,
    )


def create_job_category_for_testcase(name: str) -> JobCategory:
    return JobCategory.objects.create(
        display_name=name,
        name=name,
        description=name,
    )
