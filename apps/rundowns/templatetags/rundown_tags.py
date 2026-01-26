from django import template


register = template.Library()


@register.simple_tag()
def get_total_duration():
    return "123"


@register.filter(name="times")
def times(number):
    return range(0, number + 1)
