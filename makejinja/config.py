import typing as t
from pathlib import Path

import rich_click as click
import typed_settings as ts
from jinja2.defaults import (
    BLOCK_END_STRING,
    BLOCK_START_STRING,
    COMMENT_END_STRING,
    COMMENT_START_STRING,
    VARIABLE_END_STRING,
    VARIABLE_START_STRING,
)


@ts.settings(frozen=True)
class Delimiter:
    block_start: str = t.cast(
        str,
        ts.option(
            default=BLOCK_START_STRING,
        ),
    )
    block_end: str = t.cast(
        str,
        ts.option(
            default=BLOCK_END_STRING,
        ),
    )
    comment_start: str = t.cast(
        str,
        ts.option(
            default=COMMENT_START_STRING,
        ),
    )
    comment_end: str = t.cast(
        str,
        ts.option(
            default=COMMENT_END_STRING,
        ),
    )
    variable_start: str = t.cast(
        str,
        ts.option(
            default=VARIABLE_START_STRING,
        ),
    )
    variable_end: str = t.cast(
        str,
        ts.option(
            default=VARIABLE_END_STRING,
        ),
    )


@ts.settings(frozen=True)
class Config:
    input_path: Path = t.cast(
        Path,
        ts.option(
            click={"type": click.Path(exists=True, file_okay=False, path_type=Path)},
            help="""
                Path to a folder containing template files.
                It is passed to Jinja's [FileSystemLoader](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.FileSystemLoader) when creating the environment.
            """,
        ),
    )
    output_path: Path = t.cast(
        Path,
        ts.option(
            click={"type": click.Path(file_okay=False, writable=True, path_type=Path)},
            help="""
                Path to a folder where the rendered templates are stored.
                makejinja preserves the relative paths in the process, meaning that you can even use it on nested directories.
            """,
        ),
    )
    input_pattern: str = t.cast(
        str,
        ts.option(
            default="**/*",
            help="""
                Glob pattern to search for files in `input_folder`.
                Accepts all pattern supported by [`fnmatch`](https://docs.python.org/3/library/fnmatch.html#module-fnmatch).
                If a file is matched by this pattern and does not end with the specified `jinja-suffix`, it is copied over to the `output_folder`.
                **Note:** Do not add a special suffix used by your template files here, instead use the `jinja-suffix` option.
            """,
        ),
    )
    jinja_suffix: str = t.cast(
        str,
        ts.option(
            default=".jinja",
            help="""
                File ending of Jinja template files.
                All files with this suffix in `input_folder` matched by `pattern` are passed to the Jinja renderer.
                **Note:** Should be provided *with* the leading dot.
            """,
        ),
    )
    data_paths: list[Path] = t.cast(
        list[Path],
        ts.option(
            factory=list,
            click={
                "type": click.Path(exists=True, path_type=Path),
                "param_decls": ("--data-path",),
            },
            help="""
                Load variables from yaml/yml or toml files for use in your Jinja templates.
                The defintions are passed to Jinja's `render` function.
                Can either be a file or a folder containg files.
                **Note:** This option may be passed multiple times to pass a list of values.
                If multiple files are supplied, beware that previous declarations will be overwritten by newer ones.
            """,
        ),
    )
    global_paths: list[Path] = t.cast(
        list[Path],
        ts.option(
            factory=list,
            click={
                "type": click.Path(exists=True, path_type=Path),
                "param_decls": ("--global-path",),
            },
            help="""
                You can import functions/varibales defined in `.py` files to use them in your Jinja templates.
                Can either be a file or a folder containg files.
                **Note:** This option may be passed multiple times to pass a list of files/folders.
                If multiple files are supplied, beware that previous declarations will be overwritten by newer ones.
            """,
        ),
    )
    filter_paths: list[Path] = t.cast(
        list[Path],
        ts.option(
            factory=list,
            click={
                "type": click.Path(exists=True, path_type=Path),
                "param_decls": ("--filter-path",),
            },
            help="""
                Jinja has support for filters (e.g., `[1, 2, 3] | length`) to easily call functions.
                This option allows you to define [custom filters](https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters) in `.py` files.
                Can either be a file or a folder containg files.
                **Note:** This option may be passed multiple times to pass a list of files/folders.
                If multiple files are supplied, beware that previous declarations will be overwritten by newer ones.
            """,
        ),
    )
    extension_names: list[str] = t.cast(
        list[str],
        ts.option(
            factory=list,
            click={"param_decls": ("--extension-name",)},
            help="""
                Extend Jinja's parser by loading the specified extensions.
                An overview of the built-in ones can be found on the [project website](https://jinja.palletsprojects.com/en/3.1.x/extensions/).
                Currently, only those built-in filters are allowed.
                **Note:** This option may be passed multiple times to pass a list of values.
            """,
        ),
    )
    lstrip_blocks: bool = t.cast(
        bool,
        ts.option(
            default=True,
            help="""
                The lstrip_blocks option can also be set to strip tabs and spaces from the beginning of a line to the start of a block.
                (Nothing will be stripped if there are other characters before the start of the block.)
                Refer to the [Jinja docs](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control) for more details.
            """,
        ),
    )
    trim_blocks: bool = t.cast(
        bool,
        ts.option(
            default=True,
            help="""
                If an application configures Jinja to trim_blocks, the first newline after a template tag is removed automatically (like in PHP).
                Refer to the [Jinja docs](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control) for more details.
            """,
        ),
    )
    keep_trailing_newline: bool = t.cast(
        bool,
        ts.option(
            default=False,
            click={
                "param_decls": ("--keep-trailing-newline/--remove-trailing-newline",)
            },
            help="""
                By default, Jinja also removes trailing newlines. To keep single trailing newlines, configure Jinja to keep_trailing_newline.
                Refer to the [Jinja docs](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control) for more details.
            """,
        ),
    )
    delimiter: Delimiter = t.cast(Delimiter, ts.option(factory=Delimiter))
    copy_tree: bool = t.cast(
        bool,
        ts.option(
            default=False,
            click={"param_decls": ("--copy-tree", "flag"), "is_flag": True},
            help="""
                If your `input_folder` containes additional files besides Jinja templates, you may want to copy them to `output_folder` as well.
                This operation maintains the metadata of all files and folders, meaning that tools like `rsync` will treat them exactly like the original ones.
                **Note:** Even if set to `no-copy-tree`, files that are matched by your provided `pattern` within `input_folder` are still copied over.
                In both cases, a file's metadata is untouched.
                The main difference is that with `copy-tree`, folders keep their metadata while matched files are copied to newly-created subfolders that differ in their metadata.
            """,
        ),
    )
    keep_jinja_suffix: bool = t.cast(
        bool,
        ts.option(
            default=False,
            click={"param_decls": ("--keep-jinja-suffix", "flag"), "is_flag": True},
            help="""
                Decide whether the specified `jinja-suffix` is removed from the file after rendering.
            """,
        ),
    )
    keep_empty: bool = t.cast(
        bool,
        ts.option(
            default=False,
            click={"param_decls": ("--keep-empty", "flag"), "is_flag": True},
            help="""
                Some Jinja template files may be empty after rendering (e.g., if they only contain macros that are imported by other templates).
                By default, we do not copy such empty files.
                If there is a need to have them available anyway, you can adjust that.
            """,
        ),
    )


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
                "--data-path",
                "--global-path",
                "--filter-path",
                "--extension-name",
            ],
        },
        {
            "name": "Jinja Whitespace Control",
            "options": ["--lstrip-blocks", "--trim-blocks", "--keep-trailing-newline"],
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
    ]
}
