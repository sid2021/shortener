"""Module with util functions."""

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def is_url_valid(url) -> bool:
    """Return True if given url is valid else False."""
    if not url:
        return False

    try:
        URLValidator()(url)
    except ValidationError:
        return False
    else:
        return True
