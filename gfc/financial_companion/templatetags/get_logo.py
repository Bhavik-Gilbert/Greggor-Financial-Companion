from django import template
from ..helpers import GreggorTypes
import os
import holidays
import datetime
from .targets import get_overall_completeness

register = template.Library()


@register.filter
def get_greggor(greggor_type: str = ""):
    """Returns the filepath for the wanted greggor logo"""

    base_path: str = os.path.join("greggor", "greggor-")
    greggor_type: str = greggor_type.lower()

    if len(greggor_type) != 0 and greggor_type in iter(GreggorTypes):
        return f"{base_path}{greggor_type}.png"

    if datetime.datetime.today().strftime(
            '%Y-%m-%d') in holidays.country_holidays('UK'):
        return f"{base_path}{GreggorTypes.PARTY}.png"

    if datetime.time(4, 0, 0) >= datetime.datetime.now().time(
    ) or datetime.datetime.now().time() >= datetime.time(22, 0, 0):
        # TODO: Make sleepy greggor
        return f"{base_path}{GreggorTypes.SAD}.png"

    # TODO: Add other greggor types
    return f"{base_path}{GreggorTypes.NORMAL}.png"

@register.filter
def get_greggor_type_from_completeness(completeness):
    """Returns the desired type of greggor based on the level of completeness of a target"""
    if completeness >= 90:
        return "party"
    elif completeness < 15:
        return "distraught"
    elif completeness < 35:
        return "sad"
    else:
        return "normal"

@register.filter
def get_greggor_type_for_overall_completeness(targets):
    """Returns the desired type of greggor based on the average completeness of all the targets"""

    overall_completeness = get_overall_completeness(targets)
    return get_greggor_type_from_completeness(overall_completeness)
