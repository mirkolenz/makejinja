import typing as t
from urllib.parse import quote as urlparse

from makejinja.typing import Filters, Globals


def hassurl(value: str) -> str:
    return urlparse(value).replace("_", "-")


def getlang(
    value: t.Union[str, t.Mapping[str, str]], lang: str, default_lang: str = "en"
):
    if isinstance(value, str):
        return value
    else:
        return value.get(lang, value.get(default_lang, ""))


class Loader:
    def filters(self) -> Filters:
        return [hassurl]

    def globals(self) -> Globals:
        return [getlang]
