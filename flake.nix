{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    systems.url = "github:nix-systems/default";
    flocken = {
      url = "github:mirkolenz/flocken/v2";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:adisbladis/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs =
    inputs@{
      self,
      nixpkgs,
      flake-parts,
      systems,
      flocken,
      pyproject-nix,
      uv2nix,
      ...
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = import systems;
      imports = [
        inputs.flake-parts.flakeModules.easyOverlay
        inputs.treefmt-nix.flakeModule
      ];
      perSystem =
        {
          pkgs,
          system,
          lib,
          config,
          ...
        }:
        let
          inherit (config.legacyPackages) pythonSet;
        in
        {
          _module.args.pkgs = import nixpkgs {
            inherit system;
            overlays = lib.singleton (
              final: prev: {
                python3 = final.python312;
                uv = uv2nix.packages.${system}.uv-bin;
              }
            );
          };
          overlayAttrs = {
            inherit (config.packages) makejinja;
          };
          checks = pythonSet.makejinja.passthru.tests // {
            inherit (pythonSet.makejinja.passthru) docs;
          };
          treefmt = {
            projectRootFile = "flake.nix";
            programs = {
              ruff-check.enable = true;
              ruff-format.enable = true;
              nixfmt.enable = true;
            };
          };
          legacyPackages.pythonSet = pkgs.callPackage ./default.nix {
            inherit (inputs) uv2nix pyproject-nix;
          };
          packages = {
            inherit (pythonSet.makejinja.passthru) docs;
            default = config.packages.makejinja;
            makejinja = pythonSet.mkApp "optionals";
            docker = pkgs.dockerTools.streamLayeredImage {
              name = "makejinja";
              tag = "latest";
              created = "now";
              config.Entrypoint = [ (lib.getExe config.packages.makejinja) ];
            };
            release-env = pkgs.buildEnv {
              name = "release-env";
              paths = with pkgs; [
                uv
                python3
              ];
            };
          };
          apps.docker-manifest.program = flocken.legacyPackages.${system}.mkDockerManifest {
            github = {
              enable = true;
              token = "$GH_TOKEN";
            };
            version = builtins.getEnv "VERSION";
            imageStreams = with self.packages; [
              x86_64-linux.docker
              aarch64-linux.docker
            ];
          };
          devShells.default = pkgs.mkShell {
            packages = with pkgs; [
              uv
              config.treefmt.build.wrapper
            ];
            UV_PYTHON = lib.getExe pkgs.python3;
            shellHook = ''
              uv sync --all-extras --locked
            '';
          };
        };
    };
}
