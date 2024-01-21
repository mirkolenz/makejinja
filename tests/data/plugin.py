from collections import abc
from pathlib import Path
from urllib.parse import quote

import makejinja


def hassurl(value: str) -> str:
    return quote(value).replace("_", "-")


def getlang(value: str | abc.Mapping[str, str], lang: str, default_lang: str = "en"):
    if isinstance(value, str):
        return value
    else:
        return value.get(lang, value.get(default_lang, ""))


class Plugin(makejinja.plugin.Plugin):
    def filters(self) -> makejinja.plugin.Filters:
        return [hassurl]

    def functions(self) -> makejinja.plugin.Functions:
        return [getlang]

    def path_filters(self) -> makejinja.plugin.PathFilters:
        return [self._remove_secrets]

    def _remove_secrets(self, path: Path) -> bool:
        if "secret" in path.stem:
            return False

        return True
