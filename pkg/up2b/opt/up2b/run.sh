#!/bin/sh

venv_dir=$HOME/.config/up2b/venv

if [ ! -d $venv_dir ]; then
    python3 -m venv $venv_dir
    # 不升级 pip 无法安装 pyqt5
    $venv_dir/bin/python -m pip install pip --upgrade -i https://mirrors.bfsu.edu.cn/pypi/web/simple
    $venv_dir/bin/python -m pip install 'pywebview[qt]' up2b 'flask[async]' -i https://mirrors.bfsu.edu.cn/pypi/web/simple
fi

$venv_dir/bin/python /opt/up2b/main.py