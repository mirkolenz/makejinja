"""
**[🌟 GitHub Project 🌟](https://github.com/mirkolenz/makejinja)**

![makejinja demonstration](../../assets/demo.gif)

.. include:: ../../README.md
   :start-after: <!-- PDOC_START -->

## Usage as a Library

While mainly intended to be used as a command line tool, makejinja can also be from Python directly.
"""

from . import cli, config, plugin
from .app import makejinja

loader = plugin

__all__ = ["makejinja", "config", "plugin", "loader", "cli"]
