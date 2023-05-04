{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-parts.url = "github:hercules-ci/flake-parts";
    devenv = {
      url = "github:cachix/devenv";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = inputs@{ nixpkgs, flake-parts, devenv, poetry2nix, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ devenv.flakeModule ];
      systems = nixpkgs.lib.systems.flakeExposed;
      perSystem = { pkgs, system, ... }:
      let
        inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication;
        py = pkgs.python311;
      in
      {
        packages.default = mkPoetryApplication {
          projectDir = ./.;
          preferWheels = true;
          python = py;
        };
        devenv.shells.default = {
          name = "makejinja";
          languages.python = {
            enable = true;
            package = py;
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
