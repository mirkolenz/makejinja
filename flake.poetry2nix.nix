{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = { self, nixpkgs, utils, poetry2nix }:
    utils.lib.eachDefaultSystem (system:
      let
        inherit (poetry2nix.legacyPackages.${system}) mkPoetryEnv overrides;
        pkgs = nixpkgs.legacyPackages.${system};
        env = mkPoetryEnv {
          projectDir = ./.;
          python = pkgs.python311;
          overrides = overrides.withDefaults (self: super: {
            rich-click = super.rich-click.overridePythonAttrs (
              old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ]; }
            );
            typed-settings = super.typed-settings.overridePythonAttrs (
              old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling ]; }
            );
          });
        };
        poetry = poetry2nix.packages.${system}.poetry;
      in {
        devShells.default = pkgs.mkShell {
          packages = [ env poetry ];
        };
      }
    );
}
