{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };
  outputs = inputs@{ flake-parts, nixpkgs, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = nixpkgs.lib.systems.flakeExposed;
      perSystem = {config, pkgs, system, ...}: {
        devShells.default =
          let
            python = pkgs.python311;
          in
          pkgs.mkShell {
            packages = [ pkgs.poetry python ];
            shellHook = ''
              poetry env use ${python}/bin/python
              poetry install --all-extras
            '';
          };
      };
    };
}
