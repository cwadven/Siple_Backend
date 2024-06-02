from common.common_criteria.cursor_criteria import CursorCriteria


class HomeProjectListCursorCriteria(CursorCriteria):
    cursor_keys = [
        'id__lt',
        'rearrangement_time__lte',
    ]
