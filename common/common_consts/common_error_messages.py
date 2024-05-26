from common.common_consts.common_enums import StrValueLabel


class ErrorMessage(StrValueLabel):
    INVALID_INPUT_ERROR_MESSAGE = ('invalid_input', '유효하지 않은 입력값입니다.')


class InvalidInputResponseErrorStatus(StrValueLabel):
    INVALID_INPUT_HOME_LIST_PARAM_ERROR_400 = (
        '400-invalid_home_list_input_error-00001', ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label
    )
