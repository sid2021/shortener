from typing import Optional

import pytest

from shortener.utils import is_url_valid


@pytest.mark.parametrize(
    "url, expected_result",
    [
        ("https://www.google.com", True),
        ("https://www.amazon.com/foo/bar/baz", True),
        ("http:www.wp.xyz", False),
        ("slick.gg", False),
        ("http://localhost.com", True),
        (None, False),
        (1, False),
        ("foo", False),
    ],
)
def test_is_url_valid_returns_correct_bool(
    url: Optional[str], expected_result: bool
) -> None:
    """Ensure that is_url_valid() function returns correct bool value
    given valid and ivalid urls.
    """
    returned_value = is_url_valid(url)
    assert returned_value == expected_result
