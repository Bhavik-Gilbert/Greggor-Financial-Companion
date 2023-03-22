from django import template

register = template.Library()


@register.filter
def divide(a: float, b: float) -> float:
    """Divides number by another"""
    if (b != 0):
        return float(a / b)
    else:
        return 0


@register.filter
def sig_figs(number: float, sig_fig: int) -> float:
    """
    Returns number to a given number of significant figures
    """
    if (sig_fig > 0):
        round_to_sig_figs = float(('%.' + str(sig_fig) + 'g') % number)
        return round_to_sig_figs
    else:
        return number
