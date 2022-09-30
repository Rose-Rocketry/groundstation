{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  nativeBuildInputs = [
    pkgs.python39Packages.paho-mqtt
    pkgs.python39Packages.pyproj
    pkgs.python39Packages.flask
    pkgs.python39Packages.construct
    pkgs.python39Packages.pyserial-asyncio
    pkgs.docker-compose_2
    pkgs.yapf
  ];
}
