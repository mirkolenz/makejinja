FROM nixos/nix

WORKDIR /app

COPY poetry.lock pyproject.toml flake.lock flake.nix ./
RUN nix --extra-experimental-features "nix-command flakes" develop --impure -c true

COPY makejinja ./makejinja

ENTRYPOINT ["./.venv/bin/python", "-m", "makejinja"]
CMD ["--help"]
