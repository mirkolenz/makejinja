from collections import abc
from pathlib import Path
from typing import Any, Protocol

from jinja2 import Environment
from jinja2.ext import Extension

from makejinja.config import Config

__all__ = ["Plugin"]


type Extensions = abc.Sequence[type[Extension]]
type Filter = abc.Callable[..., Any]
type Filters = abc.Sequence[Filter]
type Function = abc.Callable[..., Any]
type Functions = abc.Sequence[Function]
type Test = abc.Callable[..., Any]
type Tests = abc.Sequence[Test]
type Policies = abc.Mapping[str, Any]
type MutableData = abc.MutableMapping[str, Any]
type Data = abc.Mapping[str, Any]
type PathFilter = abc.Callable[[Path], bool]
type PathFilters = abc.Sequence[PathFilter]


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
