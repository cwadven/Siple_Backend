from django.contrib.auth.models import UserManager

from common.common_utils import generate_random_string_digits
from member.consts import (
    SocialLoginModuleSelector,
    MemberStatusEnum,
    MemberTypeEnum,
)
from member.utils.social_utils import SocialLoginHandler


class MemberManager(UserManager):
    def get_or_create_member_by_token(self, token: str, provider: int) -> tuple:
        data = SocialLoginHandler(
            SocialLoginModuleSelector(int(provider)).selector()
        ).validate(token)

        return self.get_or_create(
            username=data['id'],
            member_provider_id=provider,
            defaults={
                'member_type_id': MemberTypeEnum.NORMAL_MEMBER.value,
                'member_status_id': MemberStatusEnum.NORMAL_MEMBER.value,
                'email': data['email'] or '',
                'nickname': data['nickname'] or f'Random{generate_random_string_digits(5)}',
            }
        )
