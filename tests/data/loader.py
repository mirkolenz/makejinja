from collections import abc
from urllib.parse import quote


def hassurl(value: str) -> str:
    return quote(value).replace("_", "-")


def getlang(value: str | abc.Mapping[str, str], lang: str, default_lang: str = "en"):
    if isinstance(value, str):
        return value
    else:
        return value.get(lang, value.get(default_lang, ""))


class Loader:
    def filters(self):
        return [hassurl]

    def functions(self):
        return [getlang]
