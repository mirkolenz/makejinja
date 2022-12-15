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

<!-- Regenerate: COLUMNS=120 py makejinja --help | pbcopy -->
