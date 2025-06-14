<!-- markdownlint-disable MD033 MD041 -->
<h1><p align="center">makejinja</p></h1>

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
  Generate entire directory structures using Jinja templates with support for external data and custom plugins.
</p>

<p align="center">
  <img alt="makejinja demonstration" src="https://mirkolenz.github.io/makejinja/assets/demo.gif" />
</p>

---

<!-- PDOC_START -->

makejinja can be used to automatically generate files from [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates).
It is conceptually similar to [Ansible templates](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html) since both are built on top of Jinja.
However, makejinja is a standalone tool that can be used without Ansible and offers some advanced features like custom plugins.

A popular use case is generating config files for [Home Assistant](https://www.home-assistant.io/):
Using the same Jinja language that Home Assistant's built-in templates use, you can greatly simplify your configuration management.
makejinja's custom delimiter support prevents conflicts with Home Assistant's own template syntax, while file-specific data loading enables modular dashboard and automation generation.
Our comprehensive [Home Assistant example](https://github.com/mirkolenz/makejinja/tree/main/tests/data) demonstrates dashboard generation with custom plugins, multiple data sources, and advanced template organization.

## Key Features

- **Multi-Source Data Integration**: Load variables from YAML, TOML, and Python files, with support for file-specific data sources and runtime variable injection.
- **Custom Template Delimiters**: Configure Jinja delimiters (e.g., `<% %>` instead of `{{ }}`) to avoid conflicts with target file formats like Home Assistant, Kubernetes, or Terraform.
- **Flexible Directory Processing**: Process multiple input directories with complex nested structures, preserving hierarchy while applying powerful template transformations.
- **Extensible Plugin System**: Create custom [plugins](https://mirkolenz.github.io/makejinja/makejinja/plugin.html#Plugin) with filters, functions, and path filtering logic for specialized requirements.
- **Production-Ready**: Comprehensive CLI interface, configuration file support, and Python library API for seamless workflow integration.

## Use Cases

- **Configuration Management**: Generate environment-specific configs (dev/staging/prod) from shared templates with different data sources.
- **Home Assistant Dashboards**: Create complex dashboards and automations using Jinja syntax without conflicts. See our [complete example](https://github.com/mirkolenz/makejinja/tree/main/tests/data).
- **Infrastructure as Code**: Generate Kubernetes manifests, Terraform modules, or Docker Compose files with consistent patterns across environments.
- **Web Development**: Generate HTML pages, CSS files, or JavaScript configs from data sources for static sites or multi-tenant applications.
- **Database Schemas**: Create SQL migration scripts, database configurations, or ORM models based on structured schema definitions.
- **Network Configuration**: Generate router configs, firewall rules, or network device settings from centralized network topology data.
- **Monitoring & Alerting**: Create Grafana dashboards, Prometheus rules, or alerting configurations from service inventories.
- **Documentation & CI/CD**: Create project docs, API specifications, or pipeline definitions from structured data sources.

## Installation

The tool is written in Python and can be installed via uv, nix, and docker.
It can be used as a CLI tool or as a Python library.

### UV

makejinja is available on [PyPI](https://pypi.org/project/makejinja/) and can be installed via `uv`:

```shell
uv tool install makejinja
makejinja -i ./input -o ./output
```

### Nix

makejinja is packaged in nixpkgs.
To use the most recent version, you can run it via `nix run`:

```shell
nix run github:mirkolenz/makejinja -- -i ./input -o ./output
```

Alternatively, you can add this repository as an input to your flake and use `makejinja.packages.${system}.default`.

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
