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
    makejinja(config)


if __name__ == "__main__":
    makejinja_cli()
