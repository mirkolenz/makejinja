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
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ devenv.flakeModule ];
      systems = nixpkgs.lib.systems.flakeExposed;
      perSystem = { pkgs, ... }: {
        devenv.shells.default = {
          name = "makejinja";
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
