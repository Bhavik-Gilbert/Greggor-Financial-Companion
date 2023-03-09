from django import template
from ..helpers import GreggorTypes
import os
import holidays
import datetime

register = template.Library()


@register.filter
def get_greggor(greggor_type: str = ""):
    """Returns the filepath for the wanted greggor logo"""
    base_path: str = os.path.join("greggor", "greggor-")
    greggor_type: str = greggor_type.lower()
    # print(greggor_type)
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
    if completeness >= 100:
        return "party"
    elif completeness < 50:
        return "sad"
