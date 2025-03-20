from django import template

register = template.Library()

@register.filter
def get_key(dictionary, key):
    """Returns the value of a dictionary for a given key or an empty string if not found."""
    return dictionary.get(key, "")
