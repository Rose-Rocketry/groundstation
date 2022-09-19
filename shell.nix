{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  nativeBuildInputs = [
    pkgs.python39Packages.paho-mqtt
    pkgs.python39Packages.pyproj
    pkgs.docker-compose
    pkgs.yapf
  ];
}
