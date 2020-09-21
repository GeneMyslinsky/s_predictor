#!/bin/sh

wget https://artiya4u.keybase.pub/TA-lib/ta-lib-0.4.0-src.tar.gz
tar -xvf ta-lib-0.4.0-src.tar.gz
cd /init/ta-lib/
./configure --prefix=/usr
make
make install