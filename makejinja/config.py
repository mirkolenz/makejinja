import typing as t
from pathlib import Path

import rich_click as click
import typed_settings as ts
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

__all__ = ["Config", "Delimiter", "Internal", "Prefix", "Whitespace"]


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
    line_statement: t.Optional[str] = ts.option(
        default=LINE_STATEMENT_PREFIX,
        help=(
            "If given and a string, this will be used as prefix for line based"
            " statements."
        ),
    )
    line_comment: t.Optional[str] = ts.option(
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
    input: Path = ts.option(
        click={"type": click.Path(exists=True, file_okay=False, path_type=Path)},
        help="""
            Path to a folder containing template files.
            It is passed to Jinja's [FileSystemLoader](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.FileSystemLoader) when creating the environment.
        """,
    )
    output: Path = ts.option(
        click={"type": click.Path(file_okay=False, writable=True, path_type=Path)},
        help="""
            Path to a folder where the rendered templates are stored.
            makejinja preserves the relative paths in the process, meaning that you can even use it on nested directories.
        """,
    )
    input_pattern: str = ts.option(
        default="**/*",
        help="""
            Glob pattern to search for files in `input_folder`.
            Accepts all pattern supported by [`fnmatch`](https://docs.python.org/3/library/fnmatch.html#module-fnmatch).
            If a file is matched by this pattern and does not end with the specified `jinja-suffix`, it is copied over to the `output_folder`.
            **Note:** Do not add a special suffix used by your template files here, instead use the `jinja-suffix` option.
        """,
    )
    jinja_suffix: str = ts.option(
        default=".jinja",
        help="""
            File ending of Jinja template files.
            All files with this suffix in `input_folder` matched by `pattern` are passed to the Jinja renderer.
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
    copy_tree: bool = ts.option(
        default=False,
        click={"param_decls": "--copy-tree"},
        help="""
            If your `input_folder` containes additional files besides Jinja templates, you may want to copy them to `output_folder` as well.
            This operation maintains the metadata of all files and folders, meaning that tools like `rsync` will treat them exactly like the original ones.
            **Note:** Even if set to `no-copy-tree`, files that are matched by your provided `pattern` within `input_folder` are still copied over.
            In both cases, a file's metadata is untouched.
            The main difference is that with `copy-tree`, folders keep their metadata while matched files are copied to newly-created subfolders that differ in their metadata.
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
    data: list[Path] = ts.option(
        factory=list,
        click={
            "type": click.Path(exists=True, path_type=Path),
            "param_decls": "--data",
        },
        help="""
                Load variables from yaml/yml/toml files for use in your Jinja templates.
                The defintions are passed to Jinja's `render` function.
                Can either be a file or a folder containg files.
                **Note:** This option may be passed multiple times to pass a list of values.
                If multiple files are supplied, beware that previous declarations will be overwritten by newer ones.
            """,
    )
    loaders: list[str] = ts.option(
        factory=list,
        click={
            "param_decls": "--loader",
        },
        help="""
            Use custom Python code to adjust the used Jinja environment to your needs.
            The specified Python file should export a **class** containing a subset of the following functions:
            `filters`, `globals`, `data`, and `extensions`.
            In addition, you may add an `__init__` function that recives two positional arguments:
            the created Jinja environment and the data parsed from the files supplied to makejinja's `data` option.
            This allows you to apply aribtrary logic to makejinja.
            An import path can be specified either in dotted notation (`your.custom.Loader`)
            or with a colon as object delimiter (`your.custom:Loader`).
            **Note:** This option may be passed multiple times to pass a list of values.
        """,
    )
    import_paths: list[Path] = ts.option(
        factory=lambda: [Path(".")],
        click={
            "type": click.Path(exists=True, file_okay=False, path_type=Path),
            "param_decls": "--import-path",
        },
        help="""
            In order to load custom loaders or Jinja extensions, the PYTHONPATH variable needs to be patched.
            By default, makejinja will look for modules in your current directory, but you may change that.
        """,
    )
    extensions: list[str] = ts.option(
        factory=list,
        click={"param_decls": "--extension"},
        help="""
            List of Jinja extensions to use as strings of import paths.
            An overview of the built-in ones can be found on the [project website](https://jinja.palletsprojects.com/en/3.1.x/extensions/).
            **Note:** This option may be passed multiple times to pass a list of values.
        """,
    )
    delimiter: Delimiter = ts.option(factory=Delimiter)
    prefix: Prefix = ts.option(factory=Prefix)
    whitespace: Whitespace = ts.option(factory=Whitespace)
    internal: Internal = ts.option(factory=Internal)


OPTION_GROUPS = {
    "makejinja": [
        {
            "name": "Input/Output",
            "options": [
                "--input",
                "--output",
                "--input-pattern",
                "--jinja-suffix",
                "--copy-tree",
                "--keep-jinja-suffix",
                "--keep-empty",
            ],
        },
        {
            "name": "Jinja Environment",
            "options": [
                "--data",
                "--loader",
                "--import-path",
                "--extension",
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
