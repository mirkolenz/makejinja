from collections import abc
from pathlib import Path
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

    def path_filters(self):
        return [self._remove_secrets]

    def _remove_secrets(self, path: Path) -> bool:
        if "secret" in path.stem:
            return False

        return True
