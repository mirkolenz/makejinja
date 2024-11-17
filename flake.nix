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
          workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
          pyprojectOverlay = workspace.mkPyprojectOverlay {
            sourcePreference = "wheel";
          };
          mkBuildSystemOverrides =
            attrs: final: prev:
            lib.mapAttrs (
              name: value:
              prev.${name}.overrideAttrs (old: {
                nativeBuildInputs = old.nativeBuildInputs or [ ] ++ (final.resolveBuildSystem value);
              })
            ) attrs;
          buildSystemOverrides = mkBuildSystemOverrides {
            markupsafe = {
              setuptools = [ ];
            };
            immutables = {
              setuptools = [ ];
            };
            coverage = {
              setuptools = [ ];
            };
          };
          pyprojectOverrides = final: prev: {
            makejinja = prev.makejinja.overrideAttrs (old: {
              passthru = (old.passthru or { }) // {
                tests = (old.tests or { }) // {
                  pytest = pkgs.stdenv.mkDerivation {
                    name = "${final.makejinja.name}-pytest";
                    inherit (final.makejinja) src;
                    nativeBuildInputs = [
                      (final.mkVirtualEnv "makejinja-test-env" {
                        makejinja = [ "test" ];
                      })
                    ];
                    dontConfigure = true;
                    buildPhase = ''
                      runHook preBuild
                      pytest --cov-report=html
                      runHook postBuild
                    '';
                    installPhase = ''
                      runHook preInstall
                      mv htmlcov $out
                      runHook postInstall
                    '';
                  };
                };
                docs = pkgs.stdenv.mkDerivation {
                  name = "${final.makejinja.name}-docs";
                  inherit (final.makejinja) src;
                  nativeBuildInputs = with pkgs; [
                    (final.mkVirtualEnv "makejinja-docs-env" {
                      makejinja = [ "docs" ];
                    })
                    asciinema-scenario
                    asciinema-agg
                  ];
                  dontConfigure = true;
                  buildPhase = ''
                    runHook preBuild

                    {
                      echo '```txt'
                      COLUMNS=120 makejinja --help
                      echo '```'
                    } > ./manpage.md

                    asciinema-scenario ./assets/demo.scenario > ./assets/demo.cast
                    agg \
                      --font-dir "${pkgs.jetbrains-mono}/share/fonts/truetype" \
                      --font-family "JetBrains Mono" \
                      --theme monokai \
                      ./assets/demo.cast ./assets/demo.gif

                    pdoc \
                      -d google \
                      -t pdoc-template \
                      --math \
                      --logo https://raw.githubusercontent.com/mirkolenz/makejinja/main/assets/logo.png \
                      -o "$out" \
                      ./src/makejinja

                    runHook postBuild
                  '';
                  installPhase = ''
                    runHook preInstall

                    mkdir -p "$out/assets"
                    cp -rf ./assets/{*.png,*.gif} "$out/assets/"

                    runHook postInstall
                  '';
                };
              };
            });
          };
          baseSet = pkgs.callPackage pyproject-nix.build.packages {
            python = pkgs.python3;
          };
          pythonSet = baseSet.overrideScope (
            lib.composeManyExtensions [
              pyprojectOverlay
              pyprojectOverrides
              buildSystemOverrides
            ]
          );
          addMeta =
            drv:
            drv.overrideAttrs (old: {
              passthru = lib.recursiveUpdate (old.passthru or { }) {
                inherit (pythonSet.makejinja.passthru) tests;
              };
              meta = (old.meta or { }) // {
                mainProgram = "makejinja";
                maintainers = with lib.maintainers; [ mirkolenz ];
                license = lib.licenses.mit;
                homepage = "https://github.com/mirkolenz/makejinja";
                description = "Generate entire directory structures using Jinja templates with support for external data and custom plugins.";
                platforms = with lib.platforms; darwin ++ linux;
              };
            });
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
          packages = {
            inherit (pythonSet.makejinja.passthru) docs;
            default = config.packages.makejinja;
            makejinja = addMeta (pythonSet.mkVirtualEnv "makejinja-env" workspace.deps.optionals);
            docker = pkgs.dockerTools.buildLayeredImage {
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
            images = with self.packages; [
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
