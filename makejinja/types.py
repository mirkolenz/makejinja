import typing as t
from abc import ABC, abstractmethod

from jinja2 import Environment
from jinja2.ext import Extension

ExtensionType = t.Union[Extension, str]
Extensions = t.Sequence[ExtensionType]
Filter = t.Callable[[t.Any], t.Any]
Filters = t.Sequence[Filter]
Global = t.Callable[..., t.Any]
Globals = t.Sequence[Global]
Data = t.Mapping[str, t.Any]


class ExportsTemplate(ABC):
    def filters(self) -> Filters:
        return []

    def globals(self) -> Globals:
        return []

    def data(self) -> Data:
        return {}

    def extensions(self) -> Extensions:
        return []

    def setup_env(self, env: Environment) -> None:
        pass
