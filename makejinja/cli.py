from pathlib import Path
from typing import Type, cast

import rich_click as click
import typed_settings as ts
from typed_settings.types import AttrsInstance

from makejinja.config import OPTION_GROUPS, Config

from .app import makejinja

__all__ = ["makejinja_cli"]

click.rich_click.USE_MARKDOWN = True
click.rich_click.OPTION_GROUPS = OPTION_GROUPS

_loader = ts.default_loaders(
    appname="makejinja", config_files=(Path(".makejinja.toml"),)
)


@click.command("makejinja")
@ts.click_options(cast(Type[AttrsInstance], Config), _loader)
def makejinja_cli(config: Config):
    """makejinja can be used to automatically generate files from [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates/).

    Instead of passing CLI options, you can also write them to a file called `.makejinja.toml` in your working directory.
    **Note**: In this file, options may be named differently.
    Please refer to the file [`makejinja/config.py`](https://github.com/mirkolenz/makejinja/blob/main/makejinja/config.py) to see their actual names.
    You will also find an example here: [`makejinja/tests/data/.makejinja.toml`](https://github.com/mirkolenz/makejinja/blob/main/tests/data/.makejinja.toml).
    """

    makejinja(config)


if __name__ == "__main__":
    makejinja_cli()
