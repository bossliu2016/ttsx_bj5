#coding=utf-8
from django.template import Library
register=Library()

@register.filter
def multi(num1):
    return int(num1)*-1

