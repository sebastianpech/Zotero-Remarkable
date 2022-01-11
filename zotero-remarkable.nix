{ stdenv, rmapi, python3 }:
stdenv.mkDerivation {
  name = "zotero-remarkable";
  buildInputs = [ python3 ];
  propagatedBuildInputs = [ rmapi ];
  unpackPhase = "true";
  installPhase = ''
    mkdir -p $out/bin
    cp ${./sync.py} $out/bin/zotero-remarkable
    chmod +x $out/bin/zotero-remarkable
    '';
}
