from django import template
from typing import Any

register = template.Library()


@register.filter
def get_key_list(dictionary: dict[Any, Any]) -> list[Any]:
    """Returns the list of keys for a given dictionary"""
    return [*dictionary.keys()]


@register.filter
def to_list(value: Any) -> list[Any]:
    """Puts input into a list"""
    return [value]


@register.filter
def length(list_in: list[Any]) -> int:
    """Returns the length of a given list"""
    return len(list_in)
