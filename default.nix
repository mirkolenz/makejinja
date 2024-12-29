{
  lib,
  stdenv,
  callPackage,
  fetchFromGitHub,
  python3,
  jetbrains-mono,
  asciinema-scenario,
  asciinema-agg,
  uv2nix,
  pyproject-nix,
  pyproject-build-systems,
}:
let
  pdocRepo = fetchFromGitHub {
    owner = "mitmproxy";
    repo = "pdoc";
    tag = "v15.0.1";
    hash = "sha256-HDrDGnK557EWbBQtsvDzTst3oV0NjLRm4ilXaxd6/j8=";
  };
  workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
  pyprojectOverlay = workspace.mkPyprojectOverlay {
    sourcePreference = "wheel";
  };
  pyprojectOverrides = final: prev: {
    makejinja = prev.makejinja.overrideAttrs (old: {
      meta = (old.meta or { }) // {
        mainProgram = "makejinja";
        maintainers = with lib.maintainers; [ mirkolenz ];
        license = lib.licenses.mit;
        homepage = "https://github.com/mirkolenz/makejinja";
        description = "Generate entire directory structures using Jinja templates with support for external data and custom plugins.";
        platforms = with lib.platforms; darwin ++ linux;
      };
      passthru = lib.recursiveUpdate (old.passthru or { }) {
        tests.pytest = stdenv.mkDerivation {
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
        docs = stdenv.mkDerivation {
          name = "${final.makejinja.name}-docs";
          inherit (final.makejinja) src;
          nativeBuildInputs = [
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
              --font-dir "${jetbrains-mono}/share/fonts/truetype" \
              --font-family "JetBrains Mono" \
              --theme monokai \
              ./assets/demo.cast ./assets/demo.gif

            pdoc \
              -d google \
              -t ${pdocRepo}/examples/dark-mode \
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
  baseSet = callPackage pyproject-nix.build.packages {
    python = python3;
  };
in
{
  inherit workspace;
  inherit (callPackage pyproject-nix.build.util { }) mkApplication;
  pythonSet = baseSet.overrideScope (
    lib.composeManyExtensions [
      pyproject-build-systems.overlays.default
      pyprojectOverlay
      pyprojectOverrides
    ]
  );
}
