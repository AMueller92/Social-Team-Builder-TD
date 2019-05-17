from django import template
from django.utils.safestring import mark_safe

import markdown2

register = template.Library()


@register.filter('markdown_to_html')
def markdown_to_html(text):
    '''Convert markdown to html'''
    html = markdown2.markdown(text)
    return mark_safe(html)
