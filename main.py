#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: main.py
# @Created:   2021-02-19 16:43:08
# @Modified:  2022-03-30 21:14:51

import os
import sys
import webview

from up2b.up2b_lib.utils import logger
from colorful_logger.logger import is_debug
from server import app
from server.apis import Api


def get_distro() -> str:
    if not os.path.exists("/etc/os-version"):
        return ""

    with open("/etc/os-version") as f:
        lines = f.readlines()
        lines = lines[1:]
        for line in lines:
            temp = line[:-1].split("=")
            if temp[0] == "SystemName":
                return temp[1]
    return ""


if sys.platform == "linux":
    distro = get_distro()
    if distro == "Deepin":
        os.environ["QT_SCALE_FACTOR"] = os.environ["DEEPIN_WINE_SCALE"]
    else:
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # 自动配置缩放，可能会使用不正确的缩放比例

__version__ = "0.1.0.1 beta"

api = Api()

localization = {
    "global.quitConfirmation": "你真的要退出吗？",
    # 'global.ok': u'确认',
    # 'global.quit': u'退出',
    # 'global.cancel': u'取消',
    # 'global.saveFile': u'保存文件',
    # 'cocoa.menu.about': u'关于',
    # 'cocoa.menu.services': u'服务',
    # 'cocoa.menu.view': u'View',
    # 'cocoa.menu.hide': u'隐藏',
    # 'cocoa.menu.hideOthers': u'隐藏其他',
    # 'cocoa.menu.showAll': u'显示全部',
    # 'cocoa.menu.quit': u'退出',
    # 'cocoa.menu.fullscreen': u'Enter Fullscreen',
    # 'windows.fileFilter.allFiles': u'All files',
    # 'windows.fileFilter.otherFiles': u'Other file types',
    # 'linux.openFile': u'打开文件',
    # 'linux.openFiles': u'打开多个文件',
    # 'linux.openFolder': u'打开文件夹',
}

min_width, min_height = 548, 740

debug = is_debug()
title = f"up2b {__version__} debug" if debug else f"up2b {__version__}"
index = "assets/index.html"

if sys.platform == "win32":
    # windows 的宽最少是 548 时才能保证一行能容纳三张缩略图
    min_width = 548

webview.create_window(
    title,
    app,
    width=min_width,
    height=min_height,
    min_size=(min_width, min_height),
    text_select=False,
)

with logger:
    if sys.platform == "win32":
        webview.start(debug=debug, localization=localization, gui="edgechromium")
    else:
        # use qt on deepin
        webview.start(debug=debug, localization=localization, gui="qt")
