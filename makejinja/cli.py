import importlib.util
import shutil
import sys
import typing as t
from pathlib import Path
from types import ModuleType
from uuid import uuid1 as uuid

import typer
from jinja2 import Environment, FileSystemLoader
from rich import print
from simpleconf import Config

app = typer.Typer()


def import_file(path: Path) -> ModuleType:
    # https://stackoverflow.com/a/41595552
    # https://docs.python.org/3.11/library/importlib.html#importing-a-source-file-directly
    name = str(uuid()).lower().replace("-", "")
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None

    spec.loader.exec_module(module)

    return module


def collect_files(paths: t.Iterable[Path]) -> t.List[Path]:
    files = []

    for path in paths:
        if path.is_dir():
            files.extend(
                file for file in path.iterdir() if not file.name.startswith(".")
            )
        elif path.is_file():
            files.append(path)

    return files


@app.command()
def run(
    input_folder: Path,
    output_folder: Path,
    pattern: str = "**/*",
    jinja_suffix: str = ".jinja",
    data: list[Path] = typer.Option([]),
    globals: list[Path] = typer.Option([]),
    filters: list[Path] = typer.Option([]),
    extensions: list[str] = typer.Option([]),
    data_env_prefix: str = "JINJA",
    lstrip_blocks: bool = True,
    trim_blocks: bool = True,
    keep_trailing_newline: bool = False,
    copy_tree: bool = True,
    remove_jinja_suffix: bool = True,
    skip_empty: bool = True,
):
    # Also consider env vars with specified prefix
    _data: list[t.Union[str, Path]] = [f"{data_env_prefix}.osenv"]
    _data.extend(collect_files(data))
    render_args = Config.load(*_data)

    env = Environment(
        loader=FileSystemLoader(input_folder),
        extensions=extensions,
        keep_trailing_newline=keep_trailing_newline,
        trim_blocks=trim_blocks,
        lstrip_blocks=lstrip_blocks,
    )

    for _global in collect_files(globals):
        mod = import_file(_global)
        env.globals.update(mod.globals)

    for _filter in collect_files(filters):
        mod = import_file(_filter)
        env.filters.update(mod.filters)

    if output_folder.is_dir():
        shutil.rmtree(output_folder)

    if copy_tree:
        shutil.copytree(input_folder, output_folder)

    output_folder.mkdir(parents=True, exist_ok=True)

    for input_path in input_folder.glob(pattern):
        if not input_path.is_dir():
            relative_path = input_path.relative_to(input_folder)
            output_path = output_folder / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if relative_path.suffix == jinja_suffix:
                template = env.get_template(str(relative_path))

                # Remove the copied file if the tree has been duplicated
                if copy_tree:
                    output_path.unlink()

                if remove_jinja_suffix:
                    output_path = output_path.with_suffix("")

                rendered = template.render(render_args)

                # Write the rendered template if it has content
                # Prevents empty macro definitions
                if rendered.strip() == "" and skip_empty:
                    print(f"Skip '{input_path}'")
                else:
                    print(f"Render '{input_path}'->'{output_path}'")
                    with output_path.open("w") as f:
                        f.write(rendered)

            elif not copy_tree:
                print(f"Copy '{input_path}'")
                shutil.copy2(input_path, output_path)


if __name__ == "__main__":
    app()
