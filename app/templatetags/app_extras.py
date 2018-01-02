from django import template

register = template.Library()


@register.filter
def htmlclass(total):
    if total == 1:
        return "col-lg-6 col-lg-offset-3"
    elif total == 2:
        return "col-lg-6"
    else:
        return "col-lg-4"