#!/bin/bash

# Copy and Paste each Line... this script is more like a memo
# Install needed repository if empty Kali VM
# I run pimpmykali in N mode before https://github.com/Dewalt-arch/pimpmykali

# Autoconf and Libtool are for ./bootstrap for libdaq
# CMake is for snort3
# The big line is because I am tired that there is always something missing
# The last line is because libdumbnet is missing
# yes | is to answer Y automatically BAD PRACTICE :D and -y too
yes | sudo apt-get install autoconf  
yes | sudo apt-get install libtool
yes | sudo apt-get install cmake
yes | sudo apt install build-essential cmake libboost-system-dev libboost-thread-dev libboost-program-options-dev libboost-test-dev libeigen3-dev zlib1g-dev libbz2-dev liblzma-dev
yes | sudo apt-get install libdumbnet-dev
yes | sudo apt-get install flex bison
sudo apt-get install -y libhwloc-dev
sudo apt install libluajit-5.1-dev
sudo apt-get install -y libpcap-dev 
sudo apt-get install -y libpcre3-dev libpcre3
sudo apt-get install -y cpputest 

cd $HOME
git clone https://github.com/snort3/libdaq.git
cd libdaq
./bootstrap
./configure
sudo make install # Need sudo to write file in good place
ldconfig
sudo cp /usr/local/lib/libdaq.* /usr/lib/x86_64-linux-gnu/ #http://installfights.blogspot.com/2021/01/how-to-install-snort-31-in-ubuntu-2010.html

cd $HOME
git clone https://github.com/snort3/snort3.git
cd snort3
./configure\_cmake.sh --prefix=$HOME/install/snort3 --enable-unit-tests
cd build
make -j$(nproc) install
make -j$(nproc) check

$HOME/install/snort3/bin/snort -V
$HOME/install/snort3/bin/snort --catch-test all
