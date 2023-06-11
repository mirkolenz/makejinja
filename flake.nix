{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-parts.url = "github:hercules-ci/flake-parts";
    devenv = {
      url = "github:cachix/devenv";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nix2container = {
      url = "github:nlewo/nix2container";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = inputs@{ nixpkgs, flake-parts, devenv, poetry2nix, nix2container, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ devenv.flakeModule ];
      systems = nixpkgs.lib.systems.flakeExposed;
      perSystem = { pkgs, system, lib, self', ... }:
        let
          inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication;
          inherit (nix2container.packages.${system}.nix2container) buildImage;
          py = pkgs.python311;
        in
        {
          apps.copyDockerImage = {
            type = "app";
            program = builtins.toString (pkgs.writeShellScript "copyDockerImage" ''
              IFS=$'\n' # iterate over newlines
              set -x # echo on
              for DOCKER_TAG in $DOCKER_METADATA_OUTPUT_TAGS; do
                ${lib.getExe self'.packages.dockerImage.copyTo} "docker://$DOCKER_TAG"
              done
            '');
          };
          packages = rec {
            makejinja = mkPoetryApplication {
              projectDir = ./.;
              preferWheels = true;
              python = py;
            };
            default = makejinja;
            dockerImage = buildImage {
              name = "makejinja";
              config = {
                entrypoint = [ (lib.getExe makejinja) ];
                cmd = [ "--help" ];
              };
            };

          };
          devenv.shells.default = {
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
