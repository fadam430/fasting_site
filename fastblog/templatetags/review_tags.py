from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def stars(value, max_stars=5):
    """Render a simple star rating string (filled and empty stars).

    Usage in template: {{ review.rating|stars }}
    """
    try:
        r = int(value)
    except (TypeError, ValueError):
        r = 0
    if r < 0:
        r = 0
    if r > int(max_stars):
        r = int(max_stars)
    full = '★' * r
    empty = '☆' * (int(max_stars) - r)
    return mark_safe(f"{full}{empty}")
