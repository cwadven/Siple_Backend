from common.common_exceptions import CommonAPIException


class ProjectDatabaseCreationErrorException(CommonAPIException):
    status_code = 409
    default_detail = '프로젝트 생성 중 오류가 발생했습니다.'
    default_code = 'project-creation-unknown-error'


class ProjectNotFoundErrorException(CommonAPIException):
    status_code = 404
    default_detail = '프로젝트가 존재하지 않습니다.'
    default_code = 'project-not-found-error'


class ProjectRecruitProjectNotFoundErrorException(CommonAPIException):
    status_code = 404
    default_detail = '프로젝트가 존재하지 않습니다.'
    default_code = 'project-recruit-project-not-found-error'


class ProjectLatestRecruitNotFoundErrorException(CommonAPIException):
    status_code = 404
    default_detail = '아직 모집중이 아닙니다.'
    default_code = 'project-recruit-latest-not-found-error'


class ProjectCurrentRecruitStatusNotRecruitingException(CommonAPIException):
    status_code = 400
    default_detail = '모집이 마감되었습니다.'
    default_code = 'project-recruit-not-recruiting-error'


class ProjectRecruitmentJobNotAvailableException(CommonAPIException):
    status_code = 404
    default_detail = '모집이 마감되었습니다.'
    default_code = 'project-recruit-job-not-found-error'


class ProjectRecruitmentJobRecruitingNotFoundErrorException(CommonAPIException):
    status_code = 404
    default_detail = '모집이 존재하지 않습니다.'
    default_code = 'project-recruit-job-recruiting-not-found-error'


class ProjectRecruitmentJobAlreadyRecruitedException(CommonAPIException):
    status_code = 400
    default_detail = '이미 지원한 모집입니다.'
    default_code = 'project-recruit-job-already-recruited-error'


class ProjectBookmarkMemberNotFoundException(CommonAPIException):
    status_code = 403
    default_detail = '로그인을 확인해 주세요.'
    default_code = 'project-bookmark-member-not-found-error'


class ProjectBookmarkCreationErrorException(CommonAPIException):
    status_code = 400
    default_detail = '북마크 생성 중 오류가 발생했습니다.'
    default_code = 'project-bookmark-creation-unknown-error'
