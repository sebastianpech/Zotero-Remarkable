{ stdenv, rmapi, python3 }:
stdenv.mkDerivation {
  name = "zotero-remarkable";
  buildInputs = [ python3 ];
  propagatedBuildInputs = [ rmapi ];
  unpackPhase = "true";
  installPhase = ''
    mkdir -p $out/bin
    cp ${./sync.py} $out/bin/sync.py
    chmod +x $out/bin/sync.py
    '';
}
