"""Step decorators to abstract Allure steps from test layer"""

import functools
from collections.abc import Callable
from typing import Any

import allure


def step(step_name: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to create Allure steps without importing allure in tests
    Usage: @step("Step description")
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        name = step_name or func.__name__.replace("_", " ").title()

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with allure.step(name):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def attach_data(data: str | dict | list, name: str = "data", attachment_type: str = "text") -> None:
    """
    Helper function to attach data to Allure report
    Usage: attach_data("some text", "attachment_name")
    """
    import json

    from allure_commons.types import AttachmentType

    if attachment_type.lower() == "json":
        if isinstance(data, (dict, list)):
            data = json.dumps(data, indent=2)
        allure.attach(data, name=name, attachment_type=AttachmentType.JSON)
    elif attachment_type.lower() == "html":
        allure.attach(data, name=name, attachment_type=AttachmentType.HTML)
    else:
        allure.attach(str(data), name=name, attachment_type=AttachmentType.TEXT)
