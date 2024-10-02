{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    systems.url = "github:nix-systems/default";
    flocken = {
      url = "github:mirkolenz/flocken/v2";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
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
      poetry2nix,
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
          python = pkgs.python311;
          poetry = pkgs.poetry;
          poetryAppArgs = {
            inherit python;
            projectDir = ./.;
            preferWheels = true;
            meta = {
              mainProgram = "makejinja";
              maintainers = with lib.maintainers; [ mirkolenz ];
              license = lib.licenses.mit;
              homepage = "https://github.com/mirkolenz/makejinja";
              description = "Generate entire directory structures using Jinja templates with support for external data and custom plugins.";
              platforms = lib.platforms.darwin ++ lib.platforms.linux;
            };
          };
        in
        {
          _module.args.pkgs = import nixpkgs {
            inherit system;
            overlays = [ poetry2nix.overlays.default ];
          };
          overlayAttrs = {
            inherit (config.packages) makejinja;
          };
          checks = {
            inherit (config.packages) makejinja;
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
            default = pkgs.poetry2nix.mkPoetryApplication (poetryAppArgs // { checkPhase = "pytest"; });
            makejinja = config.packages.default;
            docker = pkgs.dockerTools.buildLayeredImage {
              name = "makejinja";
              tag = "latest";
              created = "now";
              config = {
                entrypoint = [ (lib.getExe config.packages.default) ];
                cmd = [ ];
              };
            };
            releaseEnv = pkgs.buildEnv {
              name = "release-env";
              paths = [
                poetry
                python
              ];
            };
            docs =
              let
                app = pkgs.poetry2nix.mkPoetryApplication (poetryAppArgs // { groups = [ "docs" ]; });
                env = app.dependencyEnv;
                font = pkgs.jetbrains-mono;
              in
              pkgs.stdenv.mkDerivation {
                name = "makejinja-docs";
                src = ./.;
                buildPhase = ''
                  mkdir -p "$out"

                  {
                    echo '```txt'
                    COLUMNS=120 ${lib.getExe app} --help
                    echo '```'
                  } > ./manpage.md

                  # remove everything before the first ---
                  # ${lib.getExe pkgs.gnused} -i '1,/^---$/d' ./README.md
                  # remove everything before the first header
                  ${lib.getExe pkgs.gnused} -i '1,/^# /d' ./README.md

                  ${lib.getExe pkgs.asciinema-scenario} ./assets/demo.scenario > ./assets/demo.cast
                  ${lib.getExe pkgs.asciinema-agg} \
                    --font-dir "${font}/share/fonts/truetype" \
                    --font-family "JetBrains Mono" \
                    --theme monokai \
                    ./assets/demo.cast ./assets/demo.gif

                  ${lib.getExe' env "pdoc"} -d google -t pdoc-template --math \
                    --logo https://raw.githubusercontent.com/mirkolenz/makejinja/main/assets/logo.png \
                    -o "$out" ./makejinja

                  mkdir "$out/assets"
                  cp -rf ./assets/{*.png,*.gif} "$out/assets/"
                '';
                dontInstall = true;
              };
          };
          legacyPackages.dockerManifest = flocken.legacyPackages.${system}.mkDockerManifest {
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
            packages = [
              poetry
              python
              pkgs.vhs
              config.treefmt.build.wrapper
            ];
            POETRY_VIRTUALENVS_IN_PROJECT = true;
            shellHook = ''
              ${lib.getExe poetry} env use ${lib.getExe python}
              ${lib.getExe poetry} install --sync --all-extras --no-root
            '';
          };
        };
    };
}
