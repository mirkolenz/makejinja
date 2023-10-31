<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img width="256px" src="./assets/logo.png" />
</p>
<p align="center">
  <a href="./docs/install.md">Installation</a> |
  <a href="./docs/manpage.md">Usage</a> |
  <a href="./tests/data">Example</a> |
  <a href="https://jinja.palletsprojects.com/en/3.1.x/templates">Templating</a>
</p>
<p align="center">
  makejinja is a CLI tool and Python library to automatically generate files from templates.
</p>

---

# makejinja

makejinja can be used to automatically generate files from [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates).
This allows you to load variables from external files or create repeating patterns via loops.
It is conceptually similar to [gomplate](https://github.com/hairyhenderson/gomplate), but is built on Python and Jinja instead of Go.
A use case for this tool is generating config files for [Home Assistant](https://www.home-assistant.io/):
Using the same language that the built-in templates use, you can greatly simplify your configuration.
An [example for Home Assistant](./tests/data) can be found in the tests directory.

## Features

- Recursively convert nested directories containing template files. One can even specify a pattern to specify relevant files in a folder.
- Load data files containing variables to use in your Jinja templates from YAML, TOML, and Python files.
- Use custom functions in your Jinja templates by loading custom filters and/or globals.
- Easily load bundled as well as custom Jinja extensions.
- Tailor the whitespace behavior to your needs.
- Use custom delimiters for Jinja blocks/comments/variables.
- Modify _all_ init options for the Jinja environment.
- Write custom **Python loaders** that implement a subset of our fully typed [abstract loader class](./makejinja/loader.py)

## Installation and Usage

The tool is written in Python and can be installed via pip, nix, and docker.
It can be used as a CLI tool or as a Python library.
Please refer to the [installation instructions](./docs/install.md) for details.

In its default configuration, makejinja searches the input folder recursively for files ending in `.jinja`.
It then renders these files and writes them to the output folder, preserving the directory structure.
The [manpage](./docs/manpage.md) contains a detailed description of all options and can also be accessed via `makejinja --help`.
