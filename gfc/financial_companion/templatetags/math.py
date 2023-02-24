from django import template
import decimal

register = template.Library()

@register.filter
def divide(a,b):
    return float(a / b)

@register.filter
def sig_figs(number, sig_fig):
    round_to_sig_figs = '%s' % float(('%.' + str(sig_fig) + 'e') % number)

    print(decimal.Decimal(round_to_sig_figs).as_tuple().exponent)
    if (decimal.Decimal(round_to_sig_figs).as_tuple().exponent < -(sig_fig-1)):
        round_to_sig_figs = round(float(round_to_sig_figs),int(sig_fig-1))

    return round_to_sig_figs