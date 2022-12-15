# MakeJinja

## Installation

MakeJinja is available via `pip` and can be installed via

`pip install makejinja`

Beware that depending on other packages installed on your system via pip, there may be incompatibilities.
Thus, we advise leveraging [`pipx`](https://github.com/pypa/pipx) instead:

`pipx install makejinja`

## Usage

Two arguments are required to work:

1. `INPUT_FOLDER` containing the template files. It is passed to Jinja's [`FileSystemLoader`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.FileSystemLoader) when creating the environment.
2. `OUTPUT_FOLDER` as a location where the rendered templates are stored. MakeJinja preserves the relative paths in the process, meaning that you can even use it on nested directories.

To get an overview of the remaining options, we advise you to run `makejinja --help`.
In its default configuration, MakeJinja searches the input folder recursively for files ending in `.jinja`.
Also, we copy all contents (except raw template files) of the input folder to the output folder and remove the `.jinja` ending during the render process.
