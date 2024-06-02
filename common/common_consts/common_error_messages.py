from common.common_consts.common_enums import StrValueLabel


class ErrorMessage(StrValueLabel):
    INVALID_INPUT_ERROR_MESSAGE = ('invalid_input', '유효하지 않은 입력값입니다.')
    INVALID_COMPARE_ERROR_NEED_TO_BE_BIGGER = ('invalid_compare_bigger', '{} 값은 {} 보다 커야합니다.')
    INVALID_COMPARE_ERROR_NEED_TO_BE_SMALLER = ('invalid_compare_smaller', '{} 값은 {} 보다 작아야합니다.')
    INVALID_MAXIMUM_LENGTH = ('invalid_maximum_length', '최대값을 초과했습니다.')


class InvalidInputResponseErrorStatus(StrValueLabel):
    INVALID_INPUT_HOME_LIST_PARAM_ERROR_400 = (
        '400-invalid_home_list_input_error-00001', ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label
    )
