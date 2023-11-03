import itertools
import json
import shutil
import sys
import tomllib
import typing as t
from inspect import signature
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.environment import load_extensions
from jinja2.utils import import_string
from rich import print

from makejinja.config import Config
from makejinja.loader import AbstractLoader

__all__ = ["makejinja"]


def makejinja(config: Config):
    """makejinja can be used to automatically generate files from [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates/)."""

    for path in config.import_paths:
        sys.path.append(str(path.resolve()))

    data = load_data(config)

    if config.output.is_dir():
        print(f"Remove output '{config.output}'")
        shutil.rmtree(config.output)

    config.output.mkdir()

    env = init_jinja_env(config)

    for loader in config.loaders:
        process_loader(loader, env, data)

    rendered_files: set[Path] = set()
    rendered_folders: dict[Path, Path] = {}

    for input_dir, include_pattern in itertools.product(
        config.inputs, config.include_patterns
    ):
        for input_path in sorted(input_dir.glob(include_pattern)):
            relative_path = input_path.relative_to(input_dir)
            output_path = generate_output_path(config, relative_path)

            if any(input_path.match(x) for x in config.exclude_patterns):
                print(f"Skip excluded '{input_path}'")

            elif input_path.is_file() and output_path not in rendered_files:
                render_path(input_path, relative_path, output_path, config, env, data)
                rendered_files.add(output_path)

            elif input_path.is_dir() and output_path not in rendered_folders:
                print(f"Create folder '{input_path}' -> '{output_path}'")
                output_path.mkdir()
                rendered_folders[output_path] = input_path

    # The metadata has to be copied after all files are rendered
    # Otherwise the mtime will be updated
    if config.copy_metadata:
        for output_path, input_path in rendered_folders.items():
            print(f"Copy metadata '{input_path}' -> '{output_path}'")
            shutil.copystat(input_path, output_path)


def generate_output_path(config: Config, relative_path: Path) -> Path:
    output_file = config.output / relative_path

    if relative_path.suffix == config.jinja_suffix and not config.keep_jinja_suffix:
        output_file = output_file.with_suffix("")

    return output_file


def init_jinja_env(config: Config) -> Environment:
    return Environment(
        loader=FileSystemLoader(config.inputs),
        extensions=config.extensions,
        block_start_string=config.delimiter.block_start,
        block_end_string=config.delimiter.block_end,
        variable_start_string=config.delimiter.variable_start,
        variable_end_string=config.delimiter.variable_end,
        comment_start_string=config.delimiter.comment_start,
        comment_end_string=config.delimiter.comment_end,
        line_statement_prefix=config.prefix.line_statement,
        line_comment_prefix=config.prefix.line_comment,
        trim_blocks=config.whitespace.trim_blocks,
        lstrip_blocks=config.whitespace.lstrip_blocks,
        newline_sequence=config.whitespace.newline_sequence,  # type: ignore
        keep_trailing_newline=config.whitespace.keep_trailing_newline,
        optimized=config.internal.optimized,
        undefined=config.undefined.value,
        finalize=None,
        autoescape=config.internal.autoescape,
        cache_size=config.internal.cache_size,
        auto_reload=config.internal.auto_reload,
        bytecode_cache=None,
        enable_async=config.internal.enable_async,
    )


def from_yaml(path: Path) -> dict[str, t.Any]:
    data = {}

    with path.open("rb") as fp:
        for doc in yaml.safe_load_all(fp):
            data |= doc

    return data


def from_toml(path: Path) -> dict[str, t.Any]:
    with path.open("rb") as fp:
        return tomllib.load(fp)


def from_json(path: Path) -> dict[str, t.Any]:
    with path.open("rb") as fp:
        return json.load(fp)


DATA_LOADERS: dict[str, t.Callable[[Path], dict[str, t.Any]]] = {
    ".yaml": from_yaml,
    ".yml": from_yaml,
    ".toml": from_toml,
    ".json": from_json,
}


def collect_files(paths: t.Iterable[Path], pattern: str = "**/*") -> t.List[Path]:
    files = []

    for path in paths:
        if path.is_dir():
            files.extend(
                file
                for file in sorted(path.glob(pattern))
                if not file.name.startswith(".") and file.is_file()
            )
        elif path.is_file():
            files.append(path)

    return files


def load_data(config: Config) -> dict[str, t.Any]:
    data: dict[str, t.Any] = {}

    for path in collect_files(config.data):
        if loader := DATA_LOADERS.get(path.suffix):
            data |= loader(path)
        else:
            print(f"Skip unsupported data '{path}'")

    return data


def process_loader(
    loader_name: str, env: Environment, data: t.MutableMapping[str, t.Any]
):
    cls: t.Type[AbstractLoader] = import_string(loader_name)
    sig_params = signature(cls).parameters
    params: dict[str, t.Any] = {}

    if sig_params.get("env"):
        params["env"] = env
    if sig_params.get("environment"):
        params["environment"] = env
    if sig_params.get("data"):
        params["data"] = data

    loader = cls(**params)

    if hasattr(loader, "extensions"):
        load_extensions(env, loader.extensions())

    if hasattr(loader, "globals"):
        env.globals.update({func.__name__: func for func in loader.globals()})

    if hasattr(loader, "filters"):
        env.filters.update({func.__name__: func for func in loader.filters()})

    if hasattr(loader, "tests"):
        env.tests.update({func.__name__: func for func in loader.tests()})

    if hasattr(loader, "policies"):
        env.policies.update(loader.policies())

    if hasattr(loader, "data"):
        data.update(loader.data())


def render_path(
    input: Path,
    relative_path: Path,
    output: Path,
    config: Config,
    env: Environment,
    data: dict[str, t.Any],
) -> None:
    if input.suffix == config.jinja_suffix:
        template = env.get_template(str(relative_path))
        rendered = template.render(data)

        # Write the rendered template if it has content
        # Prevents empty macro definitions
        if rendered.strip() == "" and not config.keep_empty:
            print(f"Skip empty '{input}'")
        else:
            print(f"Render file '{input}' -> '{output}'")
            with output.open("w") as fp:
                fp.write(rendered)

            if config.copy_metadata:
                shutil.copystat(input, output)

    else:
        print(f"Copy file '{input}' -> '{output}'")
        shutil.copy2(input, output)
