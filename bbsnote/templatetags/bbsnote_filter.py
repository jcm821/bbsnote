from django import template

register = template.Library()

# 애너테이션: 시스템이 읽는 주석
@register.filter
def sub(value, arg):
    return value - arg