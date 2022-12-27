import typing as t


def getlang(
    value: t.Union[str, t.Mapping[str, t.Any]], lang: str, default_lang: str = "en"
):
    if isinstance(value, str):
        return value
    else:
        return value.get(lang, value.get(default_lang, ""))


globals: t.Dict[str, t.Callable] = {"getlang": getlang}
