# filepath: /Users/alex_d/Dev/equipment_base/repairs/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_by_id(queryset, id):
    """
    Retrieve an object by its ID from a queryset and return its display name.
    """
    try:
        obj = queryset.get(id=id)
        if hasattr(obj, 'name'):
            return obj.name
        return str(obj)  # Fallback to string representation
    except (queryset.model.DoesNotExist, ValueError, TypeError):
        return None