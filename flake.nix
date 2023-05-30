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
        inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication mkPoetryEnv;
        poetryArgs = {
          projectDir = ./.;
          preferWheels = true;
          python = pkgs.python311;
        };
        app = mkPoetryApplication poetryArgs;
        venv = mkPoetryEnv poetryArgs;
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
          dockerImage = pkgs.dockerTools.buildImage {
            name = "makejinja";
            tag = "latest";
            created = "now";
            config = {
              entrypoint = [(lib.getExe app)];
              cmd = ["--help"];
            };
          };
        };
        devShells.default = pkgs.mkShell {
          shellHook = ''
            ln -sfn ${venv} .venv
          '';
          packages = [venv pkgs.poetry];
        };
      };
    };
}
