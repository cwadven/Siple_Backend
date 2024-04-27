from common.common_consts.common_enums import StrValueLabel


class VoteStatus(StrValueLabel):
    READY = ('READY', '아직 시작 안함')
    VOTING = ('VOTING', '투표 중')
    FINISHED = ('FINISHED', '투표 종료')
    CANCELED = ('CANCELED', '투표 취소')


class VoteAnswerReferencePKTypes(StrValueLabel):
    DEFAULT_SELECTION = ('DEFAULT_SELECTION', '기본 선택 동의 비동의')
    MEMBER_ATTRIBUTE = ('MEMBER_ATTRIBUTE', '회원 속성')


class VoteRewardTargetType(StrValueLabel):
    MEMBER = ('MEMBER', '회원')


class VoteRewardStorageType(StrValueLabel):
    PROJECT = ('PROJECT', '프로젝트')
    MEMBER_ATTRIBUTE = ('MEMBER_ATTRIBUTE', '성격')


class VoteRewardAppliedStatus(StrValueLabel):
    NOT_APPLIED = ('NOT_APPLIED', '미적용')
    APPLIED = ('APPLIED', '적용됨')
    ROLLBACK = ('ROLLBACK', '취소됨')
