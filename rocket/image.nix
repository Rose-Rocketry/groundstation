# { pkgs ? import <nixpkgs> { } }:
# let
#   python-with-my-packages = pkgs.python3.withPackages (p: with p; [
#     pyserial
#     construct
#     # other python packages you want
#   ]);
# in
# python-with-my-packages.env

{ pkgs ? import <nixpkgs> { }
, pkgsLinux ? pkgs.pkgsCross.raspberryPi.pkgsStatic
}:

pkgs.dockerTools.buildImage {
  name = "hello-docker";
  config = {
    Cmd = [ "${pkgsLinux.python3}/bin/python" "-c" "print(\"Hello World!\")" ];
  };
}
