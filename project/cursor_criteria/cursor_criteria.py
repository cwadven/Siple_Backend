from common.common_criteria.cursor_criteria import CursorCriteria


class HomeProjectListCursorCriteria(CursorCriteria):
    cursor_keys = [
        'id__lt',
        'rearrangement_time__lte',
    ]


class MyProjectBookmarkListCursorCriteria(CursorCriteria):
    cursor_keys = [
        'updated_at__lt',
    ]
