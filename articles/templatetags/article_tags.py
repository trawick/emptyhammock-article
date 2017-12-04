from django import template
from django.utils.html import strip_tags

register = template.Library()


@register.filter()
def truncate_content(content, args):
    args = args or ''
    args = args.split(',')
    approx_max_length, absolute_max_length = map(int, args)
    if content[:3] == '<p>':
        try:
            end_p = content.index('</p>')
            content = content[:end_p]
        except:  # noqa
            pass
    content = strip_tags(content)
    if len(content) > absolute_max_length:
        return content[:absolute_max_length - 1] + '\u2026'  # HORIZONTAL ELLIPSIS
    return content
