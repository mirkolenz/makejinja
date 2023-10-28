# Installation

## PIP

makejinja is available via `pip` and can be installed via

`pip install makejinja`

Beware that depending on other packages installed on your system via pip, there may be incompatibilities.
Thus, we advise leveraging [`pipx`](https://github.com/pypa/pipx) instead:

`pipx install makejinja`

You can then directly invoke the app as follows:

`makejinja --input ./data/input --output ./data/output`

## Nix

If you use the `nix` package manager, you can add this repository as an input to your flake and use `makejinja.packages.${system}.default`.
You can also run it directly

`nix run github:mirkolenz/makejinja -- --input ./data/input --output ./data/output`

## Docker

We automatically publish an image at `ghcr.io/mirkolenz/makejinja`.
To use it, mount a folder to the container and pass the options as the command.

`docker run --rm -v $(pwd)/data:/data ghcr.io/mirkolenz/makejinja:latest --input /data/input --output /data/output`
