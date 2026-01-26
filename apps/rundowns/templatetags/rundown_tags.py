from django import template


register = template.Library()


@register.simple_tag()
def get_total_duration():
    return "123"


@register.filter(name="format_duration")
def format_duration(duration):
    if not isinstance(duration, str):

        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
