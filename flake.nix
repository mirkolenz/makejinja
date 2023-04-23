{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };
  outputs = inputs@{ flake-parts, nixpkgs, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = nixpkgs.lib.systems.flakeExposes;
      perSystem = {config, pkgs, system, ...}: {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [ python311 ];
        };
      };
    };
}
