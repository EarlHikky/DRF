from django import template
from kpi.models import *

register = template.Library()

@register.simple_tag(name='getsales')
def get_records():
    return Sales.objects.all()

@register.simple_tag(name='getstaff')
def get_staff():
    return Staff.objects.all()


