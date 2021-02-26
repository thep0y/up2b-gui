#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@aliyun.com
# @File Name: main.py
# @Created: 2021-02-19 16:43:08
# @Modified: 2021-02-26 16:45:50

import os
import sys
import webview

from apis import Api

if sys.platform == "linux":
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # 自动配置缩放，可能会使用不正确的缩放比例
    os.environ["QT_SCALE_FACTOR"] = "1.5"

__version__ = "0.0.3alpha"

api = Api()

localization = {
    'global.quitConfirmation': u'你真的要退出吗？',
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

min_width, min_height = 520, 640

if sys.platform == "win32":
    min_width = 542
    webview.create_window(
        f"TIMG {__version__}",
        "assets/index.html",
        js_api=api,
        width=min_width,
        height=min_height,
        min_size=(min_width, min_height),
        text_select=False,
    )
    webview.start(debug=False, localization=localization, gui="edgechromium")
    # webview.start(debug=False, localization=localization, gui="edgehtml")
else:
    webview.create_window(
        f"TIMG {__version__}",
        "assets/index.html",
        js_api=api,
        width=min_width,
        height=min_height,
        min_size=(min_width, min_height),
        text_select=False,
    )
    webview.start(debug=False, localization=localization)
