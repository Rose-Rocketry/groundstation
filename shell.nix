{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  nativeBuildInputs = [
    pkgs.python39Packages.paho-mqtt
    pkgs.python39Packages.pyproj
    pkgs.python39Packages.flask
    pkgs.docker-compose
    pkgs.yapf
  ];
}
