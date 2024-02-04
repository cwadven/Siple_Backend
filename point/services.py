from django.db.models import Sum
from django.db.models.functions import Coalesce
from point.exceptions import NotEnoughGuestPoints
from point.models import GuestPoint


def get_guest_available_total_point(guest_id: int) -> int:
    total_point = GuestPoint.objects.filter(
        guest_id=guest_id,
        is_active=True
    ).aggregate(
        total_point=Coalesce(Sum('point'), 0)
    ).get(
        'total_point'
    )
    return max(total_point, 0)


def use_point(guest_id: int, point: int, description: str) -> GuestPoint:
    total_point = get_guest_available_total_point(guest_id)
    if total_point < point:
        raise NotEnoughGuestPoints
    return GuestPoint.objects.create(
        guest_id=guest_id,
        point=-point,
        reason=description,
    )


def give_point(guest_id: int, point: int, reason: str) -> GuestPoint:
    return GuestPoint.objects.create(
        guest_id=guest_id,
        point=point,
        reason=reason,
    )
