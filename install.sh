#!/bin/bash

# TODO: 选择或创建新的python环境

INSTALL_DIR=$HOME/Applications/up2b

if [ ! -d $INSTALL_DIR ]; then
    mkdir -p $INSTALL_DIR
else
    rm -rf $INSTALL_DIR
fi

git clone https://github.com/thep0y/up2b-gui.git $INSTALL_DIR

DESKTOP="[Desktop Entry]\nName=up2b\nExec=python3 ${INSTALL_DIR}/main.py\nType=Application\nStartupNotify=true\nIcon=${INSTALL_DIR}/assets/up2b.png\nStartupWMClass=up2b\nCategories=Network;\n"

echo -e $DESKTOP > $INSTALL_DIR/up2b.desktop
chmod +x $INSTALL_DIR/up2b.desktop

APP_DESKTOP=$HOME/.local/share/applications/up2b.desktop

if [ -f $APP_DESKTOP ]; then
    rm $APP_DESKTOP
fi
ln -s $INSTALL_DIR/timg.desktop $APP_DESKTOP

if ! command -v pip3 >/dev/null 2>&1; then
    # TODO: 根据不同系统自动安装pip3 
    echo "需要先安装 python3 的包管理工具 pip3"
else
    # TODO: 为linux系统增加一个安装gtk和qt的选项
    pip3 install -r $INSTALL_DIR/requirements.txt
fi
