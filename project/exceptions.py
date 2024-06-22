from common.common_exceptions import CommonAPIException


class ProjectDatabaseCreationErrorException(CommonAPIException):
    status_code = 409
    default_detail = '프로젝트 생성 중 오류가 발생했습니다.'
    default_code = 'project-creation-unknown-error'
