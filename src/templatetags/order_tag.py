from django import template
register = template.Library()


@register.filter
def select(val1, val2):
  if val1 == val2:
    return 'selected'
  else:
    return ''


@register.filter
def active(val1, val2):
  if val1 == val2:
    return 'text-warning'
  else:
    return 'text-white'


@register.filter
def status_color(no):
  if no == 0:
    return '#a9a9a9'  # 'Draft'
  if no == 1:
    return '#ff7f50'  # 'Invalid'
  if no == 2:
    return "#9acd32"  # 'Sent'
  if no == 3:
    return '#00bfff'  # 'Paid'
