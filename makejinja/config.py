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


@ts.settings(frozen=True)
class Delimiter:
    block_start: str = ts.option(default=BLOCK_START_STRING)
    block_end: str = ts.option(
        default=BLOCK_END_STRING,
    )
    comment_start: str = ts.option(
        default=COMMENT_START_STRING,
    )
    comment_end: str = ts.option(
        default=COMMENT_END_STRING,
    )
    variable_start: str = ts.option(
        default=VARIABLE_START_STRING,
    )
    variable_end: str = ts.option(
        default=VARIABLE_END_STRING,
    )


@ts.settings(frozen=True)
class Prefix:
    line_statement: t.Optional[str] = ts.option(
        default=LINE_STATEMENT_PREFIX, help="TODO"
    )
    line_comment: t.Optional[str] = ts.option(default=LINE_COMMENT_PREFIX, help="TODO")


@ts.settings(frozen=True)
class Internal:
    unoptimized: bool = ts.option(
        default=False,
        click={"param_decls": "--internal-optimized", "hidden": True},
        help="TODO",
    )
    autoescape: bool = ts.option(
        default=False,
        click={"param_decls": "--internal-autoescape", "hidden": True},
        help="TODO",
    )
    cache_size: int = ts.option(default=400, click={"hidden": True}, help="TODO")
    auto_reload: bool = ts.option(default=True, click={"hidden": True}, help="TODO")
    enable_async: bool = ts.option(
        default=False,
        click={"param_decls": "--internal-enable-async", "hidden": True},
        help="TODO",
    )


@ts.settings(frozen=True)
class Whitespace:
    trim_blocks: bool = ts.option(
        default=True,
        click={"param_decls": "--trim-blocks/--no-trim-blocks"},
        help="""
                If an application configures Jinja to trim_blocks, the first newline after a template tag is removed automatically (like in PHP).
                Refer to the [Jinja docs](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control) for more details.
            """,
    )
    lstrip_blocks: bool = ts.option(
        default=True,
        click={"param_decls": "--lstrip-blocks/--no-lstrip-blocks"},
        help="""
                The lstrip_blocks option can also be set to strip tabs and spaces from the beginning of a line to the start of a block.
                (Nothing will be stripped if there are other characters before the start of the block.)
                Refer to the [Jinja docs](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control) for more details.
            """,
    )
    newline_sequence: str = ts.option(
        default=NEWLINE_SEQUENCE,
        click={"param_decls": "--newline-sequence"},
        help="TODO Literal['\\n', '\\r\\n', '\\r']",
    )
    keep_trailing_newline: bool = ts.option(
        default=KEEP_TRAILING_NEWLINE,
        click={"param_decls": "--keep-trailing-newline"},
        help="""
                By default, Jinja also removes trailing newlines. To keep single trailing newlines, configure Jinja to keep_trailing_newline.
                Refer to the [Jinja docs](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control) for more details.
            """,
    )


@ts.settings(frozen=True)
class Config:
    input_path: Path = ts.option(
        click={"type": click.Path(exists=True, file_okay=False, path_type=Path)},
        help="""
                Path to a folder containing template files.
                It is passed to Jinja's [FileSystemLoader](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.FileSystemLoader) when creating the environment.
            """,
    )
    output_path: Path = ts.option(
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
                Load variables from yaml/yml or toml files for use in your Jinja templates.
                The defintions are passed to Jinja's `render` function.
                Can either be a file or a folder containg files.
                **Note:** This option may be passed multiple times to pass a list of values.
                If multiple files are supplied, beware that previous declarations will be overwritten by newer ones.
            """,
    )
    modules: list[Path] = ts.option(
        factory=list,
        click={
            "type": click.Path(exists=True, path_type=Path),
            "param_decls": "--module",
        },
        help="""
            Load custom code into the program. TODO: More details
        """,
    )
    extensions: list[str] = ts.option(
        factory=list,
        click={"param_decls": "--extension"},
        help="""
                Extend Jinja's parser by loading the specified extensions.
                An overview of the built-in ones can be found on the [project website](https://jinja.palletsprojects.com/en/3.1.x/extensions/).
                Currently, only those built-in filters are allowed.
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
                "--input-path",
                "--output-path",
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
                "--module",
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
