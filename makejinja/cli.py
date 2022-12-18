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

app = typer.Typer(rich_markup_mode="markdown", add_completion=False)


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
                file
                for file in sorted(path.iterdir())
                if not file.name.startswith(".") and file.is_file()
            )
        elif path.is_file():
            files.append(path)

    return files


@app.command()
def run(
    input_folder: Path = typer.Argument(
        ...,
        help="""
            Path to a folder containing template files.
            It is passed to Jinja's [FileSystemLoader](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.FileSystemLoader) when creating the environment.
        """,
    ),
    output_folder: Path = typer.Argument(
        ...,
        help="""
            Path to a folder where the rendered templates are stored.
            MakeJinja preserves the relative paths in the process, meaning that you can even use it on nested directories.
        """,
    ),
    pattern: str = typer.Option(
        "**/*",
        rich_help_panel="Input File Handling",
        help="""
            Glob pattern to search for files in `input_folder`.
            Accepts all pattern supported by [`fnmatch`](https://docs.python.org/3/library/fnmatch.html#module-fnmatch).
            If a file is matched by this pattern and does not end with the specified `jinja-suffix`, it is copied over to the `output_folder`.
            **Note:** Do not add a special suffix used by your template files here, instead use the `jinja-suffix` option.
        """,
    ),
    jinja_suffix: str = typer.Option(
        ".jinja",
        rich_help_panel="Input File Handling",
        help="""
            File ending of Jinja template files.
            All files with this suffix in `input_folder` matched by `pattern` are passed to the Jinja renderer.
            **Note:** Should be provided *with* the leading dot.
        """,
    ),
    data: list[Path] = typer.Option(
        [],
        rich_help_panel="Jinja Environment Options",
        help="""
            Load variables from various file formats for use in your Jinja templates.
            The defintions are passed to Jinja's `render` function.
            Can either be a file or a folder containg files.
            **Note:** This option may be passed multiple times to pass a list of values.
            If multiple files are supplied, beware that previous declarations will be overwritten by newer ones.
            The following file formats are supported:

            - `.ini/.cfg/.config` (using `iniconfig`)
            - `.env` (using `python-dotenv`)
            - `.yaml/.yml` (using `pyyaml`)
            - `.toml` (using `rtoml`)
            - `.json` (using `json`)
        """,
    ),
    data_env_prefix: str = typer.Option(
        "jinja",
        rich_help_panel="Jinja Environment Options",
        help="""
            It is possible to provide data to the templates via environment variables.
            This option allows to configure the (case-sensitive) prefix to use for this.
            **Example:** When using `--data-env-prefix jinja` and setting the env var `jinja_style`, the variable `style` will be available in your templates.
            **Note:** Environment variables are processed after all other data files, allowing you to override their contents.
        """,
    ),
    globals: list[Path] = typer.Option(
        [],
        rich_help_panel="Jinja Environment Options",
        help="""
            You can import functions/varibales defined in `.py` files to use them in your Jinja templates.
            Can either be a file or a folder containg files.
            **Note:** This option may be passed multiple times to pass a list of files/folders.
            If multiple files are supplied, beware that previous declarations will be overwritten by newer ones.
        """,
    ),
    filters: list[Path] = typer.Option(
        [],
        rich_help_panel="Jinja Environment Options",
        help="""
            Jinja has support for filters (e.g., `[1, 2, 3] | length`) to easily call functions.
            This option allows you to define [custom filters](https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters) in `.py` files.
            Can either be a file or a folder containg files.
            **Note:** This option may be passed multiple times to pass a list of files/folders.
            If multiple files are supplied, beware that previous declarations will be overwritten by newer ones.
        """,
    ),
    extensions: list[str] = typer.Option(
        [],
        rich_help_panel="Jinja Environment Options",
        help="""
            Extend Jinja's parser by loading the specified extensions.
            An overview of the built-in ones can be found on the [project website](https://jinja.palletsprojects.com/en/3.1.x/extensions/).
            **Note:** This option may be passed multiple times to pass a list of values.
        """,
    ),
    lstrip_blocks: bool = typer.Option(
        True,
        rich_help_panel="Jinja Whitespace Control",
        help="""
            The lstrip_blocks option can also be set to strip tabs and spaces from the beginning of a line to the start of a block.
            (Nothing will be stripped if there are other characters before the start of the block.)
            Refer to the [Jinja docs](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control) for more details.
        """,
    ),
    trim_blocks: bool = typer.Option(
        True,
        rich_help_panel="Jinja Whitespace Control",
        help="""
            If an application configures Jinja to trim_blocks, the first newline after a template tag is removed automatically (like in PHP).
            Refer to the [Jinja docs](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control) for more details.
        """,
    ),
    keep_trailing_newline: bool = typer.Option(
        False,
        rich_help_panel="Jinja Whitespace Control",
        help="""
            By default, Jinja also removes trailing newlines. To keep single trailing newlines, configure Jinja to keep_trailing_newline.
            Refer to the [Jinja docs](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control) for more details.
        """,
    ),
    copy_tree: bool = typer.Option(
        True,
        rich_help_panel="Output File Handling",
        help="""
            If your `input_folder` containes additional files besides Jinja templates, you may want to copy them to `output_folder` as well.
            This operation maintains the metadata of all files and folders, meaning that tools like `rsync` will treat them exactly like the original ones.
            **Note:** Even if set to `no-copy-tree`, files that are matched by your provided `pattern` within `input_folder` are still copied over.
            In both cases, a file's metadata is untouched.
            The main difference is that with `copy-tree`, folders keep their metadata while matched files are copied to newly-created subfolders that differ in their metadata.
        """,
    ),
    remove_jinja_suffix: bool = typer.Option(
        True,
        rich_help_panel="Output File Handling",
        help="""
            Decide whether the specified `jinja-suffix` is removed from the file after rendering.
        """,
    ),
    skip_empty: bool = typer.Option(
        True,
        rich_help_panel="Output File Handling",
        help="""
            Some Jinja template files may be empty after rendering (e.g., if they only contain macros that are imported by other templates).
            By default, we do not copy such empty files.
            If there is a need to have them available anyway, you can adjust that.
        """,
    ),
):
    _data = [str(path) for path in collect_files(data)]
    # Also consider env vars with specified prefix
    _data.append(f"{data_env_prefix}.osenv")
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
        print(f"Remove '{output_folder}' from previous run")
        shutil.rmtree(output_folder)

    if copy_tree:
        print(f"Copy file tree to '{output_folder}'")
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
                print(f"Copy '{input_path}'->'{output_path}'")
                shutil.copy2(input_path, output_path)


if __name__ == "__main__":
    app()
