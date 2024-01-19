from collections import abc
from pathlib import Path
from typing import Any

from jinja2 import Environment
from jinja2.ext import Extension

__all__ = (
    "AbstractLoader",
    "Environment",
    "Extension",
    "Extensions",
    "Filter",
    "Filters",
    "Function",
    "Functions",
    "Test",
    "Tests",
    "Policies",
    "MutableData",
    "Data",
    "Exclusion",
    "Exclusions",
)

Extensions = abc.Sequence[type[Extension]]
Filter = abc.Callable[[Any], Any]
Filters = abc.Sequence[Filter]
Function = abc.Callable[..., Any]
Functions = abc.Sequence[Function]
Test = abc.Callable[..., Any]
Tests = abc.Sequence[Test]
Policies = abc.Mapping[str, Any]
MutableData = abc.MutableMapping[str, Any]
Data = abc.Mapping[str, Any]
Exclusion = abc.Callable[[Path], bool]
Exclusions = abc.Sequence[Exclusion]


class AbstractLoader:
    def __init__(self, *, env: Environment, data: Data) -> None:
        pass

    def functions(self) -> Functions:
        return []

    def data(self) -> Data:
        return {}

    def filters(self) -> Filters:
        return []

    def tests(self) -> Tests:
        return []

    def policies(self) -> Policies:
        return {}

    def extensions(self) -> Extensions:
        return []

    def exclusions(self) -> Exclusions:
        return []

    # Deprecated: Use functions() and data() instead
    def globals(self) -> Functions:
        return []
