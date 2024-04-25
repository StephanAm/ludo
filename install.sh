#! /bin/bash
set -e

sudo rm -rf /usr/local/ludo
sudo mkdir /usr/local/ludo
# copy templates
sudo mkdir /usr/local/ludo/templates
sudo cp ./templates/* /usr/local/ludo/templates/

# copy python lib files files
sudo mkdir /usr/local/ludo/libs
sudo cp ./ludomain.py\
    ./ludocli.py\
    ./ludocommon.py\
    ./ludowrapper.py\
    ./ludodataclasses.py\
    ./cli_ui.py\
    ./ludopaths.py\
    /usr/local/ludo/libs
    
sudo mkdir /usr/local/ludo/libs/ludohandlers
sudo cp -r ./arghandlers /usr/local/ludo/libs/
# copy main script
sudo cp ./ludo.py /usr/local/bin/ludo