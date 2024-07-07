from member.models import MemberAttributeType


def create_member_attribute_type_for_testcase(name: str) -> MemberAttributeType:
    return MemberAttributeType.objects.create(
        display_name=name,
        name=name,
        description=name,
    )
