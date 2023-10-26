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
      in {
        _module.args.pkgs = import nixpkgs {
          inherit system;
          overlays = [poetry2nix.overlay];
        };
        packages = {
          default = pkgs.poetry2nix.mkPoetryApplication {
            inherit python;
            projectDir = ./.;
            preferWheels = true;
          };
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
          dockerManifest = flocken.legacyPackages.${system}.mkDockerManifest {
            github = {
              enable = true;
              token = builtins.getEnv "GH_TOKEN";
            };
            version = builtins.getEnv "VERSION";
            images = with self.packages; [x86_64-linux.docker aarch64-linux.docker];
          };
          releaseEnv = pkgs.buildEnv {
            name = "release-env";
            paths = [poetry python];
          };
          updateReadme = pkgs.writeShellApplication {
            name = "update-readme";
            text = ''
              ${lib.getExe pkgs.gnused} -i '/```helpme/q' README.md
              {
                COLUMNS=120 ${lib.getExe poetry} run python -m makejinja --help
                echo '```'
              } >> README.md
              ${lib.getExe pkgs.gnused} -i 's/[[:space:]]*$//' README.md
            '';
          };
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
