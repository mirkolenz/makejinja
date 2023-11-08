"""
**[🌟 GitHub Project 🌟](https://github.com/mirkolenz/makejinja)**

![Screencast demo](../assets/demo.gif)

.. include:: ../README.md

## Usage as a Library

While mainly intended to be used as a command line tool, makejinja can also be from Python directly.
"""

from . import cli, config, loader
from .app import makejinja

__all__ = ["makejinja", "config", "loader", "cli"]
