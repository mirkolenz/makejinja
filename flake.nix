{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-parts.url = "github:hercules-ci/flake-parts";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nix2container = {
      url = "github:nlewo/nix2container";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = inputs@{ nixpkgs, flake-parts, poetry2nix, nix2container, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = nixpkgs.lib.systems.flakeExposed;
      perSystem = { pkgs, system, lib, self', ... }:
        let
          inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication mkPoetryEnv;
          inherit (nix2container.packages.${system}.nix2container) buildImage;
          poetryArgs = {
            projectDir = ./.;
            preferWheels = true;
            python = pkgs.python311;
          };
          venv = mkPoetryEnv poetryArgs;
          makejinja = mkPoetryApplication poetryArgs;
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
          packages = {
            inherit makejinja;
            default = makejinja;
            dockerImage = buildImage {
              name = "makejinja";
              config = {
                entrypoint = [ (lib.getExe makejinja) ];
                cmd = [ "--help" ];
              };
            };
          };
          devShells.default = pkgs.mkShell {
            shellHook = ''
              ln -sfn ${venv} .venv
            '';
            packages = [ venv pkgs.poetry ];
          };
        };
    };
}
