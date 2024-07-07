from common.common_exceptions import CommonAPIException


class ProjectDatabaseCreationErrorException(CommonAPIException):
    status_code = 409
    default_detail = '프로젝트 생성 중 오류가 발생했습니다.'
    default_code = 'project-creation-unknown-error'


class ProjectNotFoundErrorException(CommonAPIException):
    status_code = 404
    default_detail = '프로젝트가 존재하지 않습니다.'
    default_code = 'project-not-found-error'
