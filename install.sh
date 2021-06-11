#!/bin/bash

cwd=$(pwd)
version=$(lsb_release -rs | head -c2 )

if [ "$version" != "20" ]
then
  echo "Warning! This script is only tested on Ubuntu 20 and will likely not work on other major versions."
  sleep 3
fi

# Update apt
sudo apt update

# Installing necessary packages
sudo apt install -y git python2 python3 python3-pip curl

# Get python2 pip
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2 get-pip.py
rm get-pip.py

# CPPPO Correct Version 4.0.*
sudo pip install cpppo==4.0.*

# MiniCPS
cd ~
git clone --depth 1 https://github.com/afmurillo/minicps.git || git -C minicps pull
cd minicps
sudo python2 -m pip install .

## Installing other DHALSIM dependencies
sudo pip install pathlib==1.0.*
sudo pip install pyyaml==5.3.*

# Mininet from source
cd ~
git clone --depth 1 -b 2.3.0 https://github.com/mininet/mininet.git || git -C mininet pull
cd mininet
sudo PYTHON=python2 ./util/install.sh -fnv

# Install DHALSIM
cd ${cwd}
sudo python3 -m pip install -e .
sudo service openvswitch-switch start

# Installation complete
printf "\nInstallation finished. You can now run DHALSIM by using \n\t<sudo dhalsim your_config.yaml>.\n"
