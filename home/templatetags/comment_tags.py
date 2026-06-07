from django import template

register = template.Library()

@register.filter
def ru_comments_plural(value):
  try:
      count = int(value)
  except (ValueError, TypeError):
      return f"{value} комментариев"

  n1 = count % 10
  n2 = count % 100

  if n2 >= 11 and n2 <= 19:
      return f"{count} комментариев"
  elif n1 == 1:
      return f"{count} комментарий"
  elif n1 >= 2 and n1 <= 4:
      return f"{count} комментария"
  else:
      return f"{count} комментариев"