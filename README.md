# MakeJinja

## Installation

MakeJinja is available via `pip` and can be installed via

`pip install makejinja`

Beware that depending on other packages installed on your system via pip, there may be incompatibilities.
Thus, we advise leveraging [`pipx`](https://github.com/pypa/pipx) instead:

`pipx install makejinja`

## Usage

In its default configuration, MakeJinja searches the input folder recursively for files ending in `.jinja`.
Also, we copy all contents (except raw template files) of the input folder to the output folder and remove the `.jinja` ending during the render process.
To get an overview of the remaining options, we advise you to run `makejinja --help`:

<!-- echo -e "\n```txt\n$(COLUMNS=120 poetry run makejinja --help)\n```" >> README.md -->

```txt

 Usage: makejinja [OPTIONS] INPUT_FOLDER OUTPUT_FOLDER

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    input_folder       PATH  Path to a folder containing template files. It is passed to Jinja's FileSystemLoader   │
│                               when creating the environment.                                                         │
│                               [default: None]                                                                        │
│                               [required]                                                                             │
│ *    output_folder      PATH  Path to a folder where the rendered templates are stored. MakeJinja preserves the      │
│                               relative paths in the process, meaning that you can even use it on nested directories. │
│                               [default: None]                                                                        │
│                               [required]                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Input File Handling ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --pattern             TEXT  Glob pattern to search for files in input_folder. Accepts all pattern supported by       │
│                             fnmatch. If a file is matched by this pattern and does not end with the specified        │
│                             jinja-suffix, it is copied over to the output_folder. Note: Do not add a special suffix  │
│                             used by your template files here, instead use the jinja-suffix option.                   │
│                             [default: **/*]                                                                          │
│ --jinja-suffix        TEXT  File ending of Jinja template files. All files with this suffix in input_folder matched  │
│                             by pattern are passed to the Jinja renderer. Note: Should be provided with the leading   │
│                             dot.                                                                                     │
│                             [default: .jinja]                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Jinja Environment Options ──────────────────────────────────────────────────────────────────────────────────────────╮
│ --data                   PATH  Load variables from various file formats for use in your Jinja templates. The         │
│                                defintions are passed to Jinja's render function. Can either be a file or a folder    │
│                                containg files. Note: This option may be passed multiple times to pass a list of      │
│                                values. If multiple files are supplied, beware that previous declarations will be     │
│                                overwritten by newer ones. The following file formats are supported:                  │
│                                                                                                                      │
│                                 • .ini/.cfg/.config (using iniconfig)                                                │
│                                 • .env (using python-dotenv)                                                         │
│                                 • .yaml/.yml (using pyyaml)                                                          │
│                                 • .toml (using rtoml)                                                                │
│                                 • .json (using json)                                                                 │
│ --data-env-prefix        TEXT  It is possible to provide data to the templates via environment variables. This       │
│                                option allows to configure the (case-sensitive) prefix to use for this. Example: When │
│                                using --data-env-prefix jinja and setting the env var jinja_style, the variable style │
│                                will be available in your templates. Note: Environment variables are processed after  │
│                                all other data files, allowing you to override their contents.                        │
│                                [default: jinja]                                                                      │
│ --globals                PATH  You can import functions/varibales defined in .py files to use them in your Jinja     │
│                                templates. Can either be a file or a folder containg files. Note: This option may be  │
│                                passed multiple times to pass a list of files/folders. If multiple files are          │
│                                supplied, beware that previous declarations will be overwritten by newer ones.        │
│ --filters                PATH  Jinja has support for filters (e.g., [1, 2, 3] | length) to easily call functions.    │
│                                This option allows you to define custom filters in .py files. Can either be a file or │
│                                a folder containg files. Note: This option may be passed multiple times to pass a     │
│                                list of files/folders. If multiple files are supplied, beware that previous           │
│                                declarations will be overwritten by newer ones.                                       │
│ --extensions             TEXT  Extend Jinja's parser by loading the specified extensions. An overview of the         │
│                                built-in ones can be found on the project website. Note: This option may be passed    │
│                                multiple times to pass a list of values.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Jinja Whitespace Control ───────────────────────────────────────────────────────────────────────────────────────────╮
│ --lstrip-blocks            --no-lstrip-blocks              The lstrip_blocks option can also be set to strip tabs    │
│                                                            and spaces from the beginning of a line to the start of a │
│                                                            block. (Nothing will be stripped if there are other       │
│                                                            characters before the start of the block.) Refer to the   │
│                                                            Jinja docs for more details.                              │
│                                                            [default: lstrip-blocks]                                  │
│ --trim-blocks              --no-trim-blocks                If an application configures Jinja to trim_blocks, the    │
│                                                            first newline after a template tag is removed             │
│                                                            automatically (like in PHP). Refer to the Jinja docs for  │
│                                                            more details.                                             │
│                                                            [default: trim-blocks]                                    │
│ --keep-trailing-newline    --no-keep-trailing-newline      By default, Jinja also removes trailing newlines. To keep │
│                                                            single trailing newlines, configure Jinja to              │
│                                                            keep_trailing_newline. Refer to the Jinja docs for more   │
│                                                            details.                                                  │
│                                                            [default: no-keep-trailing-newline]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Output File Handling ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ --copy-tree              --no-copy-tree                If your input_folder containes additional files besides Jinja │
│                                                        templates, you may want to copy them to output_folder as      │
│                                                        well. This operation maintains the metadata of all files and  │
│                                                        folders, meaning that tools like rsync will treat them        │
│                                                        exactly like the original ones. Note: Even if set to          │
│                                                        no-copy-tree, files that are matched by your provided pattern │
│                                                        within input_folder are still copied over. In both cases, a   │
│                                                        file's metadata is untouched. The main difference is that     │
│                                                        with copy-tree, folders keep their metadata while matched     │
│                                                        files are copied to newly-created subfolders that differ in   │
│                                                        their metadata.                                               │
│                                                        [default: copy-tree]                                          │
│ --remove-jinja-suffix    --no-remove-jinja-suffix      Decide whether the specified jinja-suffix is removed from the │
│                                                        file after rendering.                                         │
│                                                        [default: remove-jinja-suffix]                                │
│ --skip-empty             --no-skip-empty               Some Jinja template files may be empty after rendering (e.g., │
│                                                        if they only contain macros that are imported by other        │
│                                                        templates). By default, we do not copy such empty files. If   │
│                                                        there is a need to have them available anyway, you can adjust │
│                                                        that.                                                         │
│                                                        [default: skip-empty]                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
