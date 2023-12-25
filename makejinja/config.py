from collections import abc
from enum import Enum
from pathlib import Path

import immutables
import rich_click as click
import typed_settings as ts
from jinja2 import (
    ChainableUndefined,
    DebugUndefined,
    StrictUndefined,
)
from jinja2 import (
    Undefined as DefaultUndefined,
)
from jinja2.defaults import (
    BLOCK_END_STRING,
    BLOCK_START_STRING,
    COMMENT_END_STRING,
    COMMENT_START_STRING,
    KEEP_TRAILING_NEWLINE,
    LINE_COMMENT_PREFIX,
    LINE_STATEMENT_PREFIX,
    NEWLINE_SEQUENCE,
    VARIABLE_END_STRING,
    VARIABLE_START_STRING,
)

__all__ = ["Config", "Delimiter", "Internal", "Prefix", "Whitespace", "Undefined"]
frozendict = immutables.Map


class Undefined(Enum):
    default = DefaultUndefined
    chainable = ChainableUndefined
    debug = DebugUndefined
    strict = StrictUndefined


@ts.settings(frozen=True)
class Delimiter:
    block_start: str = ts.option(
        default=BLOCK_START_STRING, help="The string marking the beginning of a block."
    )
    block_end: str = ts.option(
        default=BLOCK_END_STRING, help="The string marking the end of a block."
    )
    variable_start: str = ts.option(
        default=VARIABLE_START_STRING,
        help="The string marking the beginning of a print statement.",
    )
    variable_end: str = ts.option(
        default=VARIABLE_END_STRING,
        help="The string marking the end of a print statement.",
    )
    comment_start: str = ts.option(
        default=COMMENT_START_STRING,
        help="The string marking the beginning of a comment.",
    )
    comment_end: str = ts.option(
        default=COMMENT_END_STRING, help="The string marking the end of a comment."
    )


@ts.settings(frozen=True)
class Prefix:
    line_statement: str | None = ts.option(
        default=LINE_STATEMENT_PREFIX,
        help=(
            "If given and a string, this will be used as prefix for line based"
            " statements."
        ),
    )
    line_comment: str | None = ts.option(
        default=LINE_COMMENT_PREFIX,
        help=(
            "If given and a string, this will be used as prefix for line based"
            " comments."
        ),
    )


@ts.settings(frozen=True)
class Internal:
    optimized: bool = ts.option(
        default=True,
        click={"hidden": True},
        help=(
            "Should the"
            " [optimizer](https://github.com/Pfern/jinja2/blob/master/jinja2/optimizer.py)"
            " be enabled?"
        ),
    )
    autoescape: bool = ts.option(
        default=False,
        click={"param_decls": "--internal-autoescape", "hidden": True},
        help="""
            If set to `True` the XML/HTML autoescaping feature is enabled by default.
            For more details about autoescaping see `markupsafe.Markup`.
        """,
    )
    cache_size: int = ts.option(
        default=0,
        click={"hidden": True},
        help="""
            The size of the cache.
            If the cache size is set to a positive number like `400`,
            it means that if more than 400 templates are loaded the loader will clean out the least recently used template.
            If the cache size is set to `0`, templates are recompiled all the time.
            If the cache size is `-1` the cache will not be cleaned.
        """,
    )
    auto_reload: bool = ts.option(
        default=False,
        click={"hidden": True},
        help="""
            Some loaders load templates from locations where the template sources may change (ie: file system or database).
            If `auto_reload` is set to `True`, every time a template is requested, the loader checks if the source changed and if yes,
            it will reload the template.  For higher performance it's possible to disable that.
        """,
    )
    enable_async: bool = ts.option(
        default=False,
        click={"param_decls": "--internal-enable-async", "hidden": True},
        help="""
            If set to true this enables async template execution which allows using async functions and generators.
        """,
    )


@ts.settings(frozen=True)
class Whitespace:
    trim_blocks: bool = ts.option(
        default=True,
        click={"param_decls": "--trim-blocks/--no-trim-blocks"},
        help="""
            If this is set to `True`, the first newline after a block is removed (block, not variable tag!).
        """,
    )
    lstrip_blocks: bool = ts.option(
        default=True,
        click={"param_decls": "--lstrip-blocks/--no-lstrip-blocks"},
        help="""
            If this is set to `True`, leading spaces and tabs are stripped from the start of a line to a block.
        """,
    )
    newline_sequence: str = ts.option(
        default=NEWLINE_SEQUENCE,
        click={"param_decls": "--newline-sequence"},
        help="""
            The sequence that starts a newline.
            The default is tailored for UNIX-like systems (Linux/macOS).
        """,
    )
    keep_trailing_newline: bool = ts.option(
        default=KEEP_TRAILING_NEWLINE,
        click={"param_decls": "--keep-trailing-newline"},
        help="""
            Preserve the trailing newline when rendering templates.
            The default is `False`, which causes a single newline, if present, to be stripped from the end of the template.
        """,
    )


@ts.settings(frozen=True)
class Config:
    inputs: tuple[Path, ...] = ts.option(
        click={
            "type": click.Path(exists=True, path_type=Path),
            "param_decls": ("--input", "-i"),
        },
        help="""
            Path to a folder containing template files or a single template file.
            It is passed to Jinja's [FileSystemLoader](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.FileSystemLoader) when creating the environment.
            **Note:** This option may be passed multiple times to pass a list of values.
            If a template exists in multiple inputs, the last value with be used.
        """,
    )
    output: Path = ts.option(
        click={
            "type": click.Path(path_type=Path),
            "param_decls": ("--output", "-o"),
        },
        help="""
            Path to a folder where the rendered templates are stored.
            makejinja preserves the relative paths in the process, meaning that you can even use it on nested directories.
        """,
    )
    include_patterns: tuple[str, ...] = ts.option(
        default=("**/*",),
        click={"param_decls": ("--include-pattern", "--include", "-I")},
        help="""
            Glob patterns to search for files in `inputs`.
            Accepts all pattern supported by [`fnmatch`](https://docs.python.org/3/library/fnmatch.html#module-fnmatch).
            If a file is matched by this pattern and does not end with the specified `jinja-suffix`, it is copied over to the `output_folder`.
            Multiple can be provided.
            **Note:** Do not add a special suffix used by your template files here, instead use the `jinja-suffix` option.
        """,
    )
    exclude_patterns: tuple[str, ...] = ts.option(
        default=tuple(),
        click={"param_decls": ("--exclude-pattern", "--exclude", "-E")},
        help="""
            Glob patterns pattern to exclude files matched.
            Applied against files discovered through `include_patterns`.
            Multiple can be provided.
        """,
    )
    jinja_suffix: str = ts.option(
        default=".jinja",
        help="""
            File ending of Jinja template files.
            All files with this suffix in `inputs` matched by `pattern` are passed to the Jinja renderer.
            This suffix is not enforced for individual files passed to `inputs`.
            **Note:** Should be provided *with* the leading dot.
        """,
    )
    keep_jinja_suffix: bool = ts.option(
        default=False,
        click={"param_decls": "--keep-jinja-suffix"},
        help="""
            Decide whether the specified `jinja-suffix` is removed from the file after rendering.
        """,
    )
    keep_empty: bool = ts.option(
        default=False,
        click={"param_decls": "--keep-empty"},
        help="""
            Some Jinja template files may be empty after rendering (e.g., if they only contain macros that are imported by other templates).
            By default, we do not copy such empty files.
            If there is a need to have them available anyway, you can adjust that.
        """,
    )
    copy_metadata: bool = ts.option(
        default=False,
        click={"param_decls": ("--copy-metadata", "-m")},
        help="""
            Copy the file metadata (e.g., created/modified/permissions) from the input file using `shutil.copystat`
        """,
    )
    data: tuple[Path, ...] = ts.option(
        default=tuple(),
        click={
            "type": click.Path(exists=True, path_type=Path),
            "param_decls": ("--data", "-d"),
        },
        help="""
                Load variables from yaml/yml/toml/json files for use in your Jinja templates.
                The definitions are passed to Jinja as globals.
                Can either be a file or a folder containing files.
                **Note:** This option may be passed multiple times to pass a list of values.
                If multiple files are supplied, beware that previous declarations will be overwritten by newer ones.
            """,
    )
    data_vars: abc.Mapping[str, str] = ts.option(
        default=frozendict(),
        click={
            "param_decls": ("--data-var", "-D"),
            "help": """
                Load variables from the command line for use in your Jinja templates.
                The definitions are applied after loading the data from files.
                When using dotted keys (e.g., `foo.bar=42`), the value is converted to a nested dictionary.
                Consequently, you can override values loaded from files.
                **Note:** This option may be passed multiple times.
            """,
        },
    )
    loaders: tuple[str, ...] = ts.option(
        default=tuple(),
        click={
            "param_decls": ("--loader", "-l"),
        },
        help="""
            Use custom Python code to adjust the used Jinja environment to your needs.
            The specified Python file should export a **class** containing a subset of the following functions:
            `filters`, `globals`, `data`, and `extensions`.
            In addition, you may add an `__init__` function that receives two positional arguments:
            the created Jinja environment and the data parsed from the files supplied to makejinja's `data` option.
            This allows you to apply arbitrary logic to makejinja.
            An import path can be specified either in dotted notation (`your.custom.Loader`)
            or with a colon as object delimiter (`your.custom:Loader`).
            **Note:** This option may be passed multiple times to pass a list of values.
        """,
    )
    import_paths: tuple[Path, ...] = ts.option(
        default=(Path("."),),
        click={
            "type": click.Path(exists=True, file_okay=False, path_type=Path),
            "param_decls": "--import-path",
            "show_default": "current working directory",
        },
        help="""
            In order to load custom loaders or Jinja extensions, the PYTHONPATH variable needs to be patched.
            The default value works for most use cases, but you may load other paths as well.
        """,
    )
    extensions: tuple[str, ...] = ts.option(
        default=tuple(),
        click={"param_decls": ("--extension", "-e")},
        help="""
            List of Jinja extensions to use as strings of import paths.
            An overview of the built-in ones can be found on the [project website](https://jinja.palletsprojects.com/en/3.1.x/extensions/).
            **Note:** This option may be passed multiple times to pass a list of values.
        """,
    )
    undefined: Undefined = ts.option(
        default=Undefined.default,
        help=(
            """
            Whenever the template engine is unable to look up a name or access an attribute one of those objects is created and returned.
            Some operations on undefined values are then allowed, others fail.
            The closest to regular Python behavior is `strict` which disallows all operations beside testing if it is an undefined object.
        """
        ),
    )
    clean: bool = ts.option(
        default=False,
        click={"param_decls": ("--clean", "-c")},
        help="""
            Whether to remove the output folder if it exists.
        """,
    )
    force: bool = ts.option(
        default=False,
        click={"param_decls": ("--force", "-f")},
        help="""
            Whether to overwrite existing files in the output folder.
        """,
    )
    quiet: bool = ts.option(
        default=False,
        click={"param_decls": ("--quiet", "-q")},
        help="""
            Print no information about the rendering process.
        """,
    )
    delimiter: Delimiter = Delimiter()
    prefix: Prefix = Prefix()
    whitespace: Whitespace = Whitespace()
    internal: Internal = Internal()


OPTION_GROUPS = {
    "makejinja": [
        {
            "name": "Input/Output",
            "options": [
                "--input",
                "--output",
                "--include-pattern",
                "--exclude-pattern",
                "--jinja-suffix",
                "--keep-jinja-suffix",
                "--keep-empty",
                "--copy-metadata",
            ],
        },
        {
            "name": "Jinja Environment",
            "options": [
                "--data",
                "--data-var",
                "--loader",
                "--import-path",
                "--extension",
                "--undefined",
            ],
        },
        {
            "name": "Jinja Whitespace",
            "options": [
                "--lstrip-blocks",
                "--trim-blocks",
                "--keep-trailing-newline",
                "--newline-sequence",
            ],
        },
        {
            "name": "Jinja Delimiters",
            "options": [
                "--delimiter-block-start",
                "--delimiter-block-end",
                "--delimiter-comment-start",
                "--delimiter-comment-end",
                "--delimiter-variable-start",
                "--delimiter-variable-end",
            ],
        },
        {
            "name": "Jinja Prefixes",
            "options": [
                "--prefix-line-statement",
                "--prefix-line-comment",
            ],
        },
    ]
}
