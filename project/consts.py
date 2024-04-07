from common.common_consts.common_enums import StrValueLabel


class ProjectCurrentRecruitStatus(StrValueLabel):
    RECRUITING = ('RECRUITING', '모집중')
    ADDITIONAL_RECRUITING = ('ADDITIONAL_RECRUITING', '추가 모집중')
    RECRUITED = ('RECRUITED', '모집 완료')


class ProjectStatus(StrValueLabel):
    READY = ('READY', '모집중')
    WORKING = ('WORKING', '진행중')
    FINISHED = ('FINISHED', '종료')


class ProjectResultStatus(StrValueLabel):
    FAIL = ('FAIL', '실패')
    SUCCESS = ('SUCCESS', '성공')
    CANCEL = ('CANCEL', '취소')


class ProjectJobExperienceType(StrValueLabel):
    ALL = ('ALL', '경력 무관')
    ONLY_EXPERIENCE = ('ONLY_EXPERIENCE', '경력만')


class ProjectEngagementLevel(StrValueLabel):
    MEDIUM = ('MEDIUM', '중간')
    HIGH = ('HIGH', '높음')


class ProjectResourceStatus(StrValueLabel):
    ACTIVE = ('ACTIVE', '활성')
    DELETED = ('DELETED', '삭제')


class ProjectManagementPermissionBehavior(StrValueLabel):
    PROJECT_UPDATE = ('PROJECT_UPDATE', '프로젝트 업데이트')
    PROJECT_DELETE = ('PROJECT_DELETE', '프로젝트 삭제')
    PROJECT_RECRUIT = ('PROJECT_RECRUIT', '프로젝트 모집')


class ProjectManagementPermissionStatus(StrValueLabel):
    ACTIVE = ('ACTIVE', '활성')
    WAITING = ('WAITING', '대기')
    DELETED = ('DELETED', '삭제')
