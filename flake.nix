{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-22.11";
    flake-parts.url = "github:hercules-ci/flake-parts";
    devenv = {
      url = "github:cachix/devenv";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = inputs@{ nixpkgs, flake-parts, devenv, ... }:
    let
      pyproject = (builtins.fromTOML (builtins.readFile ./pyproject.toml));
    in
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ devenv.flakeModule ];
      systems = nixpkgs.lib.systems.flakeExposed;
      perSystem = { pkgs, ... }: {
        devenv.shells.default = {
          processes.makejinja = {
            exec = "python -m makejinja";
          };
          containers.processes = {
            startupCommand = "--help";
            version = pyproject.tool.poetry.version;
            registry = "docker://ghcr.io/";
          };
          languages.python = {
            enable = true;
            package = pkgs.python311;
            poetry = {
              enable = true;
              activate.enable = true;
              install.enable = true;
            };
          };
        };
      };
    };
}
