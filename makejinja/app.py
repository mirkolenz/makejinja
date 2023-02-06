import shutil
import sys
import typing as t
from inspect import signature
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.environment import load_extensions
from jinja2.utils import import_string
from rich import print

from makejinja.loader import AbstractLoader

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from makejinja.config import Config

__all__ = ["makejinja"]


def makejinja(config: Config):
    """makejinja can be used to automatically generate files from [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates/).

    Instead of passing CLI options, you can also write them to a file called `.makejinja.toml` in your working directory.
    **Note**: In this file, options may be named differently.
    Please refer to the file [`makejinja/config.py`](https://github.com/mirkolenz/makejinja/blob/main/makejinja/config.py) to see their actual names.
    You will also find an example here: [`makejinja/tests/data/.makejinja.toml`](https://github.com/mirkolenz/makejinja/blob/main/tests/data/.makejinja.toml).
    """

    for path in config.import_paths:
        sys.path.append(str(path.resolve()))

    data = load_data(config)
    env = init_jinja_env(config)

    for loader in config.loaders:
        process_loader(loader, env, data)

    if config.output.is_dir():
        print(f"Remove '{config.output}' from previous run")
        shutil.rmtree(config.output)

    if config.copy_tree:
        print(f"Copy file tree '{config.input}' -> '{config.output}'")
        shutil.copytree(config.input, config.output)

    config.output.mkdir(parents=True, exist_ok=True)

    for input in config.input.glob(config.input_pattern):
        if not input.is_dir():
            render_file(input, config, env, data)


def init_jinja_env(config: Config) -> Environment:
    return Environment(
        loader=FileSystemLoader(config.input),
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
        # undefined: t.Type[Undefined] = Undefined,
        # finalize: t.Optional[t.Callable[..., t.Any]] = None,
        autoescape=config.internal.autoescape,
        cache_size=config.internal.cache_size,
        auto_reload=config.internal.auto_reload,
        # bytecode_cache: t.Optional["BytecodeCache"] = None,
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


DATA_LOADERS: dict[str, t.Callable[[Path], dict[str, t.Any]]] = {
    ".yaml": from_yaml,
    ".yml": from_yaml,
    ".toml": from_toml,
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


def render_file(input: Path, config: Config, env: Environment, data: dict[str, t.Any]):
    relative_path = input.relative_to(config.input)
    output = config.output / relative_path
    output.parent.mkdir(parents=True, exist_ok=True)

    if relative_path.suffix == config.jinja_suffix:
        template = env.get_template(str(relative_path))

        # Remove the copied file if the tree has been duplicated
        if config.copy_tree:
            output.unlink()

        if not config.keep_jinja_suffix:
            output = output.with_suffix("")

        rendered = template.render(data)

        # Write the rendered template if it has content
        # Prevents empty macro definitions
        if rendered.strip() == "" and not config.keep_empty:
            print(f"Skip '{input}'")
        else:
            print(f"Render '{input}' -> '{output}'")
            with output.open("w") as f:
                f.write(rendered)

    elif not config.copy_tree:
        print(f"Copy '{input}' -> '{output}'")
        shutil.copy2(input, output)
