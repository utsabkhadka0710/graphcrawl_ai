import pytest

from graphcrawl_ai.utils.safe_cast import safe_cast
from graphcrawl_ai.exceptions.crawler.crawl_url_exceptions import InvalidDataError

@pytest.mark.parametrize(
    "value, expected",
    [
        (5,5),
        (4.63, 5),
        (9.0, 9),
        ("8", 8),
        ("5.34", 6),
        (None, None),
    ],
    ids = ["valid-int", "valid-float", "valid-float-no-round-up-required",
           "valid-numeric-string", "valid-float-as-string","None-pass-through"]
)
def test_safe_cast_success_cases(value, expected):
    """Verify that valid numbers, float decimals, and numeric strings are converted cleanly into integers."""
    assert safe_cast(value=value, param_name="foo") == expected

@pytest.mark.parametrize(
    "value",
    [
        "bar",
        "1.S",
        "None",
        "",
        "   ",
        "3.5.2",
        "3..47",
        "5..",
        "6. 56",
        [1],
        {'value':7},
        (6,),
        {5.67}

    ],
    ids = ["non-numeric-string", "alpha-numeric-string", "None-as-string",
           "empty-string", "empty-whitespaces-string", "malformed_decimal_multi-dot",
           "malformed_decimal_consecutive-dot", "malformed_decimal_trailing-dot",
           "malformed_decimal_spaces", "list", "dict", "tuple",'set']
)
def test_safe_cast_failure_cases(value):
    """Verify that un-castable data structures, text words, and broken decimal strings trigger an InvalidDataError."""
    with pytest.raises(InvalidDataError):
        safe_cast(value=value, param_name="foo")