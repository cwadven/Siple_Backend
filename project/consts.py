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
