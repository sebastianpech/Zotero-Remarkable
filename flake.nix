{
  description = "Zotero-Remarkable";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    let
      devShell = {mkShell, rmapi}:
        mkShell {
          buildINputs = [
            rmapi
          ];
        };
      localOverlay = final: prev: {
        zotero-remarkable = prev.callPackage ./zotero-remarkable.nix { };
        devShell = prev.callPackage devShell { };
      };
      pkgsForSystem = system: import nixpkgs {
        overlays = [
          localOverlay
        ];
        inherit system;
      };
    in utils.lib.eachSystem [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" ] (system: rec {
      legacyPackages = pkgsForSystem system;
      packages = utils.lib.flattenTree {
        inherit (legacyPackages) devShell zotero-remarkable;
      };
      defaultPackage = packages.zotero-remarkable;
      apps.zotero-remarkable = utils.lib.mkApp { drv = packages.zotero-remarkable; };
    }) // {
      overlay = localOverlay;
      overlays = [];
    };
}
