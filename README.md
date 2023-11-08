<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img width="256px" src="https://raw.githubusercontent.com/mirkolenz/makejinja/main/assets/logo.png" />
</p>
<p align="center">
  <a href="https://pypi.org/project/makejinja/">PyPI</a> |
  <a href="https://mirkolenz.github.io/makejinja">Docs</a> |
  <a href="https://github.com/mirkolenz/makejinja/tree/main/tests/data">Example</a> |
  <a href="https://jinja.palletsprojects.com/en/3.1.x/templates">Templating</a>
</p>
<p align="center">
  makejinja is a CLI tool and Python library to automatically generate files from Jinja2 templates.
  Use it to easily generate complex Home Assistant dashboards!
</p>

---

# makejinja

makejinja can be used to automatically generate files from [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates).
This allows you to load variables from external files or create repeating patterns via loops.
It is conceptually similar to [gomplate](https://github.com/hairyhenderson/gomplate), but is built on Python and Jinja instead of Go.
A use case for this tool is generating config files for [Home Assistant](https://www.home-assistant.io/):
Using the same language that the built-in templates use, you can greatly simplify your configuration.
An [example for Home Assistant](https://github.com/mirkolenz/makejinja/tree/main/tests/data) can be found in the tests directory.

## Features

- Recursively convert nested directories containing template files. One can even specify a pattern to specify relevant files in a folder.
- Load data files containing variables to use in your Jinja templates from YAML, TOML, and Python files.
- Use custom functions in your Jinja templates by loading custom filters and/or globals.
- Easily load bundled as well as custom Jinja extensions.
- Tailor the whitespace behavior to your needs.
- Use custom delimiters for Jinja blocks/comments/variables.
- Modify _all_ init options for the Jinja environment.
- Write custom **Python loaders** that implement a subset of our fully typed [abstract loader class](https://mirkolenz.github.io/makejinja/makejinja/loader.html#AbstractLoader)

## Installation

The tool is written in Python and can be installed via pip, nix, and docker.
It can be used as a CLI tool or as a Python library.

### PIP

makejinja is available via `pip` and can be installed via

`pip install makejinja`

Beware that depending on other packages installed on your system via pip, there may be incompatibilities.
Thus, we advise leveraging [`pipx`](https://github.com/pypa/pipx) instead:

`pipx install makejinja`

You can then directly invoke the app as follows:

`makejinja -i ./input -o ./output`

### Nix

If you use the `nix` package manager, you can add this repository as an input to your flake and use `makejinja.packages.${system}.default`.
You can also run it directly

`nix run github:mirkolenz/makejinja -- -i ./input -o ./output`

### Docker

We automatically publish an image at `ghcr.io/mirkolenz/makejinja`.
To use it, mount a folder to the container and pass the options as the command.

`docker run --rm -v $(pwd)/data:/data ghcr.io/mirkolenz/makejinja:latest -i /data/input -o /data/output`

## Usage in Terminal / Command Line

In its default configuration, makejinja searches the input folder recursively for files ending in `.jinja`.
It then renders these files and writes them to the output folder, preserving the directory structure.
Our [documentation](https://mirkolenz.github.io/makejinja/makejinja/cli.html) contains a detailed description of all options and can also be accessed via `makejinja --help`.
