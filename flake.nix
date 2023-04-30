{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-22.11";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };
  outputs = inputs@{ nixpkgs, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = nixpkgs.lib.systems.flakeExposed;
      perSystem = { pkgs, ... }: {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [ poetry python311 ];
          shellHook = with pkgs; ''
            ${poetry}/bin/poetry env use ${python311}/bin/python
            ${poetry}/bin/poetry install --all-extras --no-root --no-interaction
          '';
        };
      };
    };
}
