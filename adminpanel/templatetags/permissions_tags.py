# app/templatetags/permissions_tags.py
from django import template

register = template.Library()

@register.filter
def has_permission(user, code):
    """Check user permission in templates"""
    if hasattr(user, "has_permission"):
        return user.has_permission(code)
    return False
