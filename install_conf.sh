#! /bin/sh

CONFIG_FILE=/etc/webiopi/config
HOME=/usr/share/webiopi/htdocs/

cp config $CONFIG_FILE
cp config.html $HOME
cp index.html $HOME
cp light.py $HOME

/./etc/init.d/webiopi restart
