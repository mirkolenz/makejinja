<!-- markdownlint-disable MD033 MD041 -->
<h2><p align="center">makejinja</p></h2>
<p align="center">
  <img width="256px" alt="makejinja logo" src="https://raw.githubusercontent.com/mirkolenz/makejinja/main/assets/logo.png" />
</p>
<p align="center">
  <a href="https://pypi.org/project/makejinja/">PyPI</a> |
  <a href="https://github.com/users/mirkolenz/packages/container/package/makejinja">Docker</a> |
  <a href="https://mirkolenz.github.io/makejinja">Docs</a> |
  <a href="https://github.com/mirkolenz/makejinja/tree/main/tests/data">Example</a> |
  <a href="https://jinja.palletsprojects.com/en/3.1.x/templates">Jinja reference</a>
</p>
<p align="center">
  Generate entire directory structures using Jinja templates with support for external data and custom functionality.
</p>

---

# makejinja

makejinja can be used to automatically generate files from [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates).
It is conceptually similar to [Ansible templates](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html) since both are built on top of Jinja.
However, makejinja is a standalone tool that can be used without Ansible and offers some advanced features like custom plugins.
A use case for this tool is generating config files for [Home Assistant](https://www.home-assistant.io/):
Using the same language that the built-in templates use, you can greatly simplify your configuration.
An [example for Home Assistant](https://github.com/mirkolenz/makejinja/tree/main/tests/data) can be found in the tests directory.

## Highlights

- Recursively render nested directories containing template files to a common output directory.
- Load data files containing variables to use in your Jinja templates from YAML, TOML, and Python files.
- Write custom [plugins](https://mirkolenz.github.io/makejinja/makejinja/plugin.html#Plugin) to extend the functionality of makejinja.
- Adjust all Jinja options (e.g., whitespace behavior and delimiters) to your needs via CLI flags or a config file.

## Installation

The tool is written in Python and can be installed via pip, nix, and docker.
It can be used as a CLI tool or as a Python library.

### PIP

makejinja is available on [PyPI](https://pypi.org/project/makejinja/) and can be installed via `pip`:

```shell
pip install makejinja
makejinja -i ./input -o ./output
```

### Nix

If you use the `nix` package manager, you can add this repository as an input to your flake and use `makejinja.packages.${system}.default` or apply the overlay `makejinja.overlays.default`.
You can also run it directly as follows:

```shell
nix run github:mirkolenz/makejinja -- -i ./input -o ./output
```

### Docker

We automatically publish an image to the [GitHub Container Registry](https://ghcr.io/mirkolenz/makejinja).
To use it, mount a directory to the container and pass the options as the command:

```shell
docker run --rm -v $(pwd)/data:/data ghcr.io/mirkolenz/makejinja:latest -i /data/input -o /data/output
```

## Usage in Terminal / Command Line

In its default configuration, makejinja searches the input directory recursively for files ending in `.jinja`.
It then renders these files and writes them to the output directory, preserving the directory structure.
Our [documentation](https://mirkolenz.github.io/makejinja/makejinja/cli.html) contains a detailed description of all options and can also be accessed via `makejinja --help`.
