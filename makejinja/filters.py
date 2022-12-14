import typing as t
from urllib.parse import quote as urlparse


def hassurl(value: str) -> str:
    return urlparse(value).replace("_", "-")


filters: dict[str, t.Callable[[t.Any], t.Any]] = {"hassurl": hassurl}
