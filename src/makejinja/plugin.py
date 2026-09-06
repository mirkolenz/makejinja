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
    """Extend makejinja by implementing any subset of the plugin methods.

    The optional constructor receives supported parameters by keyword.
    It may request `env` (or `environment`), `data`, and `config`.
    Configure the environment before loading any templates, including changes to
    `finalize`, custom loaders, or bytecode caching.
    """

    def __init__(self, *, env: Environment, data: Data, config: Config) -> None:
        pass

    def functions(self) -> Functions:
        """Return global template callables registered by their function names."""
        return []

    def data(self) -> Data:
        """Return global template values that override existing values."""
        return {}

    def filters(self) -> Filters:
        """Return template filters registered by their function names."""
        return []

    def tests(self) -> Tests:
        """Return template tests registered by their function names."""
        return []

    def policies(self) -> Policies:
        """Return overrides for Jinja environment policies."""
        return {}

    def extensions(self) -> Extensions:
        """Return Jinja extension classes to register on the environment."""
        return []

    def path_filters(self) -> PathFilters:
        """Return predicates that exclude discovered paths when they return false."""
        return []

    def globals(self) -> Functions:
        """Return global callables.

        Deprecated:
            Use `functions()` and `data()` instead.
        """
        return []


AbstractLoader = Plugin
