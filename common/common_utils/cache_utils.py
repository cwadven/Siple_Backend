from typing import Any

from django.core.cache import cache


def generate_dict_value_by_key_to_cache(key: str, value: dict, expire_seconds: int) -> None:
    cache.set(key, value, expire_seconds)


def get_cache_value_by_key(key: str) -> Any:
    return cache.get(key)
