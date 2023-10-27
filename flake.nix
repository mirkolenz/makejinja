{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    systems.url = "github:nix-systems/default";
    flocken = {
      url = "github:mirkolenz/flocken/v2";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = inputs @ {
    self,
    nixpkgs,
    flake-parts,
    systems,
    flocken,
    poetry2nix,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = import systems;
      perSystem = {
        pkgs,
        system,
        lib,
        self',
        ...
      }: let
        python = pkgs.python311;
        poetry = pkgs.poetry;
        poetryArgs = {
          inherit python;
          projectDir = ./.;
          preferWheels = true;
        };
      in {
        _module.args.pkgs = import nixpkgs {
          inherit system;
          overlays = [poetry2nix.overlay];
        };
        # https://msfjarvis.dev/posts/writing-your-own-nix-flake-checks/
        # https://github.com/nix-community/poetry2nix/blob/master/tests/env/default.nix
        checks.default = let
          env = pkgs.poetry2nix.mkPoetryEnv poetryArgs;
        in
          pkgs.runCommand "pytest" {} ''
            mkdir "$out" && cd "$out"
            ln -s ${self}/* .
            ${lib.getExe' env "pytest"}
          '';
        packages = {
          default = pkgs.poetry2nix.mkPoetryApplication poetryArgs;
          makejinja = self'.packages.default;
          docker = pkgs.dockerTools.buildLayeredImage {
            name = "makejinja";
            tag = "latest";
            created = "now";
            config = {
              entrypoint = [(lib.getExe self'.packages.default)];
              cmd = [];
            };
          };
          releaseEnv = pkgs.buildEnv {
            name = "release-env";
            paths = [poetry python];
          };
          updateReadme = pkgs.writeShellApplication {
            name = "update-readme";
            text = ''
              # remove everything after the manpage code block
              ${lib.getExe pkgs.gnused} -i '/```manpage/q' README.md
              # update the manpage code block
              {
                COLUMNS=120 ${lib.getExe poetry} run python -m makejinja --help
                echo '```'
              } >> README.md
              # remove trailing whitespace
              ${lib.getExe pkgs.gnused} -i 's/[[:space:]]*$//' README.md
            '';
          };
        };
        legacyPackages.dockerManifest = flocken.legacyPackages.${system}.mkDockerManifest {
          github = {
            enable = true;
            token = builtins.getEnv "GH_TOKEN";
          };
          version = builtins.getEnv "VERSION";
          images = with self.packages; [x86_64-linux.docker aarch64-linux.docker];
        };
        devShells.default = pkgs.mkShell {
          packages = [poetry python self'.packages.updateReadme];
          POETRY_VIRTUALENVS_IN_PROJECT = true;
          shellHook = ''
            ${lib.getExe poetry} env use ${lib.getExe python}
            ${lib.getExe poetry} install --all-extras --no-root
          '';
        };
      };
    };
}
