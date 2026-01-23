from django import template


register = template.Library()


@register.simple_tag()
def get_total_duration():
    return "123"
