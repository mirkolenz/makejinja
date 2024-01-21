from collections import abc
from pathlib import Path
from typing import Any, Protocol

from jinja2 import Environment
from jinja2.ext import Extension

from makejinja.config import Config

__all__ = ["Plugin"]

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
PathFilter = abc.Callable[[Path], bool]
PathFilters = abc.Sequence[PathFilter]


class Plugin(Protocol):
    """Extend the functionality of makejinja with a plugin implementing a subset of this protocol."""

    def __init__(self, *, env: Environment, data: Data, config: Config) -> None:
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

    def path_filters(self) -> PathFilters:
        return []

    # Deprecated: Use functions() and data() instead
    def globals(self) -> Functions:
        return []


AbstractLoader = Plugin
