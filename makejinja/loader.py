import typing as t

from jinja2 import Environment
from jinja2.ext import Extension

__all__ = [
    "LoaderProtocol",
    "Environment",
    "Extension",
    "Extensions",
    "Filter",
    "Filters",
    "Global",
    "Globals",
    "Test",
    "Tests",
    "Policies",
    "MutableData",
    "Data",
]

Extensions = t.Sequence[t.Type[Extension]]
Filter = t.Callable[[t.Any], t.Any]
Filters = t.Sequence[Filter]
Global = t.Callable[..., t.Any]
Globals = t.Sequence[Global]
Test = t.Callable[..., t.Any]
Tests = t.Sequence[Test]
Policies = t.Mapping[str, t.Any]
MutableData = t.MutableMapping[str, t.Any]
Data = t.Mapping[str, t.Any]


class LoaderProtocol(t.Protocol):
    @t.overload
    def __init__(self) -> None:
        ...

    @t.overload
    def __init__(self, *, env: Environment, data: MutableData) -> None:
        ...

    def filters(self) -> Filters:
        ...

    def globals(self) -> Globals:
        ...

    def tests(self) -> Tests:
        ...

    def policies(self) -> Policies:
        ...

    def data(self) -> Data:
        ...

    def extensions(self) -> Extensions:
        ...
