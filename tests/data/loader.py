import typing as t
from urllib.parse import quote as urlparse


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
    def filters(self):
        return [hassurl]

    def globals(self):
        return [getlang]
