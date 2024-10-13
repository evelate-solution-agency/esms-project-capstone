from django import template
from datetime import timedelta


register = template.Library()

@register.filter
def format_duration(value):
    if not isinstance(value, timedelta):
        return value  # if value is not a timedelta object, return it as is
    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours:
        return f'{hours} hours'
    else:
        return f'{minutes} minutes'