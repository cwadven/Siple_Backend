from job.models import Job


def create_job_for_testcase(name: str) -> Job:
    return Job.objects.create(
        display_name=name,
        name=name,
        description=name,
    )
