#!/bin/bash

INSTALL_DIR=$HOME/Applications/timg

if [ ! -d $INSTALL_DIR ]; then
    mkdir -p $INSTALL_DIR
fi

git clone https://github.com/thep0y/timg-gui.git $INSTALL_DIR

DESKTOP="[Desktop Entry]\nName=TIMG2222\nExec=python3 ${INSTALL_DIR}/main.py\nType=Application\nStartupNotify=true\nIcon=${INSTALL_DIR}/assets/timg.png\nStartupWMClass=TIMG\nCategories=Network;\n"

echo -e $DESKTOP > $INSTALL_DIR/timg.desktop
chmod +x $INSTALL_DIR/timg.desktop

APP_DESKTOP=$HOME/.local/share/applications/timg.desktop

if [ -f $APP_DESKTOP ]; then
    rm $APP_DESKTOP
fi
ln -s $INSTALL_DIR/timg.desktop $APP_DESKTOP

if ! command -v pip3 >/dev/null 2>&1; then
    # TODO 根据不同系统自动安装pip3 
    echo "需要先安装 python3 的包管理工具 pip3 "
else
    pip3 install -r $INSTALL_DIR/requirements.txt
fi



