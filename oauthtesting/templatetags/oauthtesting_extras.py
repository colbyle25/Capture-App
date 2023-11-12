# https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/
from django import template

register = template.Library()

@register.simple_tag
def get(dictionary, key):
    return dictionary.get(key)