from django import template
import os
import holidays
import datetime

register = template.Library()

@register.filter
def get_greggor(greggor_type: str = ""):
    """Returns the filepath for the wanted greggor logo"""
    base_path = os.path.join("greggor", "greggor-")
    if len(greggor_type) != 0:
        return f"{base_path}{greggor_type}.png"
    
    if datetime.datetime.today().strftime('%Y-%m-%d') in holidays.country_holidays('UK'):
        return f"{base_path}party.png"

    if datetime.time(4, 0, 0) >= datetime.datetime.now().time() or datetime.datetime.now().time() >= datetime.time(22, 0, 0):
        # TODO: Make sleepy greggor
        return f"{base_path}sad.png"
    
    # TODO: Add other greggor types
    return f"{base_path}normal.png"