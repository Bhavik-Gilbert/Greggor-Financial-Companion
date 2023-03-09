from django import template
import decimal

register = template.Library()


@register.filter
def divide(a, b):
    if (b != 0):
        return float(a / b)
    else:
        return 0


@register.filter
def sig_figs(number, sig_fig):
    if (sig_fig > 0):
        round_to_sig_figs = float(('%.'+str(sig_fig)+'g') % number)
        return round_to_sig_figs
    
    else:
        return number
