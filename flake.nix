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
    nix2container = {
      url = "github:nlewo/nix2container";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = inputs@{ nixpkgs, flake-parts, devenv, poetry2nix, nix2container, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ devenv.flakeModule ];
      systems = nixpkgs.lib.systems.flakeExposed;
      perSystem = { pkgs, system, lib, ... }:
        let
          inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication;
          inherit (nix2container.packages.${system}.nix2container) buildImage;
          py = pkgs.python311;
        in
        {
          packages = rec {
            makejinja = mkPoetryApplication {
              projectDir = ./.;
              preferWheels = true;
              python = py;
            };
            default = makejinja;
            docker =
              let
                metaJson = builtins.getEnv "DOCKER_METADATA_OUTPUT_JSON";
                meta = if metaJson == "" then { } else builtins.fromJSON metaJson;
              in
              buildImage {
                inherit meta;
                name = "makejinja";
                tag = "latest";
                config = {
                  entrypoint = [ (lib.getExe makejinja) ];
                  cmd = [ "--help" ];
                };
              };
            # https://yuanwang.ca/posts/push-docker-image-to-gcr-with-nix.html
            # docker = pkgs.dockerTools.buildImage {
            #   name = "makejinja";
            #   tag = "latest";
            #   config = {
            #     entrypoint = [ (lib.getExe makejinja) ];
            #     cmd = [ "--help" ];
            #   };
            # };
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
