from django import template

register = template.Library()


@register.filter
def getKeyList(dictionary):
    return [*dictionary.keys()]


@register.filter
def list(value):
    return [value]


@register.filter
def length(list_in):
    return len(list_in)
