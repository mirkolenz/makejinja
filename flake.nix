{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-22.11";
    flake-parts.url = "github:hercules-ci/flake-parts";
    devshell.url = "github:numtide/devshell";
  };
  outputs = inputs@{ nixpkgs, flake-parts, devshell, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ devshell.flakeModule ];
      systems = nixpkgs.lib.systems.flakeExposed;
      perSystem = { pkgs, ... }: {
        devshells.default.devshell = {
          packages = with pkgs; [ poetry python311 ];
          startup.default.text = with pkgs; ''
            ${poetry}/bin/poetry env use ${python311}/bin/python
            ${poetry}/bin/poetry install --all-extras --no-root --no-interaction
          '';
        };
      };
    };
}
