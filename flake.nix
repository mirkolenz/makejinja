{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    systems.url = "github:nix-systems/default";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = inputs @ {
    nixpkgs,
    flake-parts,
    poetry2nix,
    systems,
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
        inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication;
        python = pkgs.python311;
        poetry = pkgs.poetry;
        app = mkPoetryApplication {
          inherit python;
          projectDir = ./.;
          preferWheels = true;
        };
      in {
        apps.copyDockerImage = {
          type = "app";
          program = builtins.toString (pkgs.writeShellScript "copyDockerImage" ''
            IFS=$'\n' # iterate over newlines
            set -x # echo on
            for DOCKER_TAG in $DOCKER_METADATA_OUTPUT_TAGS; do
              ${lib.getExe pkgs.skopeo} --insecure-policy copy "docker-archive:${self'.packages.dockerImage}" "docker://$DOCKER_TAG"
            done
          '');
        };
        packages = {
          makejinja = app;
          default = app;
          dockerImage = pkgs.dockerTools.buildLayeredImage {
            name = "makejinja";
            tag = "latest";
            created = "now";
            config = {
              entrypoint = [(lib.getExe app)];
              cmd = ["--help"];
            };
          };
          releaseEnv = pkgs.buildEnv {
            name = "release-env";
            paths = [poetry python];
          };
        };
        devShells.default = pkgs.mkShell {
          packages = [poetry python];
          POETRY_VIRTUALENVS_IN_PROJECT = true;
          shellHook = ''
            ${lib.getExe poetry} env use ${lib.getExe python}
            ${lib.getExe poetry} install --all-extras --no-root
          '';
        };
      };
    };
}
