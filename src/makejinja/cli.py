"""
.. include:: ../../manpage.md
"""

from pathlib import Path

import rich_click as click
import typed_settings as ts

from makejinja.config import OPTION_GROUPS, Config

from .app import makejinja

__all__: list[str] = []

click.rich_click.USE_MARKDOWN = True
click.rich_click.OPTION_GROUPS = OPTION_GROUPS

_ts_loaders = ts.default_loaders(
    appname="makejinja", config_files=(Path("makejinja.toml"),)
)


@click.command("makejinja", context_settings={"help_option_names": ("--help", "-h")})
@click.version_option(None, "--version", "-v")
@ts.click_options(Config, _ts_loaders)
def makejinja_cli(config: Config):
    """makejinja can be used to automatically generate files from [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates/).

    Instead of passing CLI options, you can also write them to a file called `makejinja.toml` in your working directory.
    **Note**: In this file, options may be named differently.
    Please refer to the file [`makejinja/config.py`](https://github.com/mirkolenz/makejinja/blob/main/makejinja/config.py) to see their actual names.
    You will also find an example here: [`makejinja/tests/data/makejinja.toml`](https://github.com/mirkolenz/makejinja/blob/main/tests/data/makejinja.toml).
    To override its location, you can set the environment variable `MAKEJINJA_SETTINGS` to the path of your config file.
    """

    makejinja(config)


if __name__ == "__main__":
    makejinja_cli()
