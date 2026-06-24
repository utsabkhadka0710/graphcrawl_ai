import math
from typing import Any, Optional
from graphcrawl_ai.exceptions.crawler.crawl_url_exceptions import InvalidDataError

def safe_cast(value: Any, param_name: str) -> Optional[int]:
    """
    Converts the input value to a ceil-rounded integer.

    Args:
        value (Any): The input value to convert.
        param_name (str): A string representing the parameter name.

    Returns:
        Optional[int]: The converted ceil-rounded integer or None if the input is None.

    Raises:
        InvalidDataError: If the conversion fails due to invalid data type.
    """
    if value is None:
        return None

    try:
        float_value = float(value)
        return math.ceil(float_value)
    except (ValueError, TypeError):
        raise InvalidDataError(param_name)