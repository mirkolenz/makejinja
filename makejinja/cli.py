import shutil
import typing as t
from pathlib import Path
from urllib.parse import quote as urlparse

import typer
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from rich import print
from simpleconf import Config

app = typer.Typer()

filters: dict[str, t.Callable[[t.Any], t.Any]] = {
    "hassurl": lambda x: urlparse(x).replace("_", "-")
}


@app.command()
def run(
    input_folder: Path,
    output_folder: Path,
    pattern: str = "**/*",
    jinja_suffix: str = ".jinja",
    remove_jinja_suffix: bool = True,
    config: list[Path] = typer.Option([]),
    extensions: list[str] = typer.Option([]),
    lstrip_blocks: bool = True,
    trim_blocks: bool = True,
    keep_trailing_newline: bool = False,
    copy_tree: bool = True,
):
    # Also consider env vars with `jinja_` prefix
    config_files: list[str | Path] = ["jinja.osenv"]

    for path in config:
        if path.is_dir():
            config_files.extend(
                file for file in path.iterdir() if not file.name.startswith(".")
            )
        elif path.is_file():
            config_files.append(path)

    data = Config.load(*config_files)

    env = Environment(
        loader=FileSystemLoader(input_folder),
        extensions=extensions,
        keep_trailing_newline=keep_trailing_newline,
        trim_blocks=trim_blocks,
        lstrip_blocks=lstrip_blocks,
    )
    env.filters.update(filters)

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
                print(f"Render '{relative_path}'")
                template = env.get_template(str(relative_path))

                # Remove the copied file if the tree has been duplicated
                if copy_tree:
                    output_path.unlink()

                if remove_jinja_suffix:
                    output_path = output_path.with_suffix("")

                # Write the rendered template
                with output_path.open("w") as f:
                    f.write(template.render(data))

            elif not copy_tree:
                print(f"Copy '{relative_path}'")
                shutil.copy2(input_path, output_path)


if __name__ == "__main__":
    app()
