# makejinja

makejinja can be used to automatically generate files from [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates/).
This allows you to load variables from external files or create repeating patterns via loops.
It is conceptually similar to [gomplate](https://github.com/hairyhenderson/gomplate), but is built on Python and Jinja instead of Go.
A use case for this tool is generating config files for [Home Assistant](https://www.home-assistant.io/):
Using the same language that the built-in templates use, you can greatly simplify your configuration.

## Home Assistant Example

[A concrete example for Home Assistant can be found in the tests directory.](./tests/data)

## Features

- Recursively convert nested directories containing template files. One can even specify a pattern to specify relevant files in a folder.
- Load data files containing variables to use in your Jinja templates from YAML, TOML, and Python files.
- Use custom functions in your Jinja templates by loading custom filters and/or globals.
- Easily load bundled as well as custom Jinja extensions.
- Tailor the whitespace behavior to your needs.
- Use custom delimiters for Jinja blocks/comments/variables.
- Modify _all_ init options for the Jinja environment.
- Write custom **Python loaders** that implement a subset of our fully typed [loader protocol class](./makejinja/loader.py)

## Installation

makejinja is available via `pip` and can be installed via

`pip install makejinja`

Beware that depending on other packages installed on your system via pip, there may be incompatibilities.
Thus, we advise leveraging [`pipx`](https://github.com/pypa/pipx) instead:

`pipx install makejinja`

Alternatively, the application can also be used via Docker.
We automatically publish an image at `ghcr.io/mirkolenz/makejinja`.
To use it, mount a folder to the container and pass the options as the command.
For example, to process files in `./data/input` and render them to `./data/output`, you could run:

`docker run --rm -v $(pwd)/data:/data ghcr.io/mirkolenz/makejinja@latest --input /data/input --output /data/output`

## Usage

In its default configuration, makejinja searches the input folder recursively for files ending in `.jinja`.
Also, we copy all contents (except raw template files) of the input folder to the output folder and remove the `.jinja` ending during the render process.
To get an overview of the remaining options, we advise you to run `makejinja --help`:

<!-- echo -e "\n```txt\n$(COLUMNS=120 poetry run makejinja --help)\n```" >> README.md -->

```txt

 Usage: makejinja [OPTIONS]

 makejinja can be used to automatically generate files from Jinja templates.
 Instead of passing CLI options, you can also write them to a file called .makejinja.toml in your working directory.
 Note: In this file, options may be named differently. Please refer to the file makejinja/config.py to see their actual
 names. You will also find an example here: makejinja/tests/data/.makejinja.toml.

╭─ Input/Output ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --input                DIRECTORY  Path to a folder containing template files. It is passed to Jinja's             │
│                                      FileSystemLoader when creating the environment.                                 │
│                                      [required]                                                                      │
│ *  --output               DIRECTORY  Path to a folder where the rendered templates are stored. makejinja preserves   │
│                                      the relative paths in the process, meaning that you can even use it on nested   │
│                                      directories.                                                                    │
│                                      [required]                                                                      │
│    --input-pattern        TEXT       Glob pattern to search for files in input_folder. Accepts all pattern supported │
│                                      by fnmatch. If a file is matched by this pattern and does not end with the      │
│                                      specified jinja-suffix, it is copied over to the output_folder. Note: Do not    │
│                                      add a special suffix used by your template files here, instead use the          │
│                                      jinja-suffix option.                                                            │
│                                      [default: **/*]                                                                 │
│    --jinja-suffix         TEXT       File ending of Jinja template files. All files with this suffix in input_folder │
│                                      matched by pattern are passed to the Jinja renderer. Note: Should be provided   │
│                                      with the leading dot.                                                           │
│                                      [default: .jinja]                                                               │
│    --copy-tree                       If your input_folder containes additional files besides Jinja templates, you    │
│                                      may want to copy them to output_folder as well. This operation maintains the    │
│                                      metadata of all files and folders, meaning that tools like rsync will treat     │
│                                      them exactly like the original ones. Note: Even if set to no-copy-tree, files   │
│                                      that are matched by your provided pattern within input_folder are still copied  │
│                                      over. In both cases, a file's metadata is untouched. The main difference is     │
│                                      that with copy-tree, folders keep their metadata while matched files are copied │
│                                      to newly-created subfolders that differ in their metadata.                      │
│    --keep-jinja-suffix               Decide whether the specified jinja-suffix is removed from the file after        │
│                                      rendering.                                                                      │
│    --keep-empty                      Some Jinja template files may be empty after rendering (e.g., if they only      │
│                                      contain macros that are imported by other templates). By default, we do not     │
│                                      copy such empty files. If there is a need to have them available anyway, you    │
│                                      can adjust that.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Jinja Environment ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --data           PATH       Load variables from yaml/yml/toml files for use in your Jinja templates. The defintions  │
│                             are passed to Jinja's render function. Can either be a file or a folder containg files.  │
│                             Note: This option may be passed multiple times to pass a list of values. If multiple     │
│                             files are supplied, beware that previous declarations will be overwritten by newer ones. │
│ --loader         TEXT       Use custom Python code to adjust the used Jinja environment to your needs. The specified │
│                             Python file should export a class containing a subset of the following functions:        │
│                             filters, globals, data, and extensions. In addition, you may add an __init__ function    │
│                             that recives two positional arguments: the created Jinja environment and the data parsed │
│                             from the files supplied to makejinja's data option. This allows you to apply aribtrary   │
│                             logic to makejinja. An import path can be specified either in dotted notation            │
│                             (your.custom.Loader) or with a colon as object delimiter (your.custom:Loader). Note:     │
│                             This option may be passed multiple times to pass a list of values.                       │
│ --import-path    DIRECTORY  In order to load custom loaders or Jinja extensions, the PYTHONPATH variable needs to be │
│                             patched. By default, makejinja will look for modules in your current directory, but you  │
│                             may change that.                                                                         │
│                             [default: .]                                                                             │
│ --extension      TEXT       List of Jinja extensions to use as strings of import paths. An overview of the built-in  │
│                             ones can be found on the project website. Note: This option may be passed multiple times │
│                             to pass a list of values.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Jinja Whitespace ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --lstrip-blocks/--no-lstrip-blocks          If this is set to True, leading spaces and tabs are stripped from the    │
│                                             start of a line to a block.                                              │
│                                             [default: lstrip-blocks]                                                 │
│ --trim-blocks/--no-trim-blocks              If this is set to True, the first newline after a block is removed       │
│                                             (block, not variable tag!).                                              │
│                                             [default: trim-blocks]                                                   │
│ --keep-trailing-newline                     Preserve the trailing newline when rendering templates. The default is   │
│                                             False, which causes a single newline, if present, to be stripped from    │
│                                             the end of the template.                                                 │
│ --newline-sequence                    TEXT  The sequence that starts a newline. The default is tailored for          │
│                                             UNIX-like systems (Linux/macOS).                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Jinja Delimiters ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --delimiter-block-start       TEXT  The string marking the beginning of a block.                                     │
│                                     [default: {%]                                                                    │
│ --delimiter-block-end         TEXT  The string marking the end of a block.                                           │
│                                     [default: %}]                                                                    │
│ --delimiter-comment-start     TEXT  The string marking the beginning of a comment.                                   │
│                                     [default: {#]                                                                    │
│ --delimiter-comment-end       TEXT  The string marking the end of a comment.                                         │
│                                     [default: #}]                                                                    │
│ --delimiter-variable-start    TEXT  The string marking the beginning of a print statement.                           │
│                                     [default: {{]                                                                    │
│ --delimiter-variable-end      TEXT  The string marking the end of a print statement.                                 │
│                                     [default: }}]                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Jinja Prefixes ─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --prefix-line-statement    TEXT  If given and a string, this will be used as prefix for line based statements.       │
│ --prefix-line-comment      TEXT  If given and a string, this will be used as prefix for line based comments.         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
