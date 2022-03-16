#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@aliyun.com
# @File Name: __init__.py
# @Created: 2021-02-19 16:42:55
# @Modified:  2022-03-11 12:53:00

import os
import webview

from typing import Dict, Union
from up2b import IMAGE_BEDS
from up2b.up2b_lib.up2b_api import CONF_FILE, choose_image_bed
from up2b.up2b_lib.up2b_api.sm import SM
from up2b.up2b_lib.up2b_api.imgtu import Imgtu
from up2b.up2b_lib.up2b_api.gitee import Gitee
from up2b.up2b_lib.up2b_api.github import Github
from up2b.up2b_lib.constants import (
    IMAGE_BEDS_CODE,
    SM_MS,
    IMGTU,
    GITEE,
    GITHUB,
    IS_WINDOWS,
)
from up2b.up2b_lib.errors import OverSizeError, UploadFailed
from apis.utils import read_config

if IS_WINDOWS:
    import ctypes


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False
        self.image_bed = None
        self.auto_compress: bool = False
        # self.conf: Dict[str, str] = read_config(CONF_FILE)
        self.height = self.width = 0
        if IS_WINDOWS:
            user32 = ctypes.windll.user32  # type: ignore
            self.width: int = user32.GetSystemMetrics(0)
            self.height: int = user32.GetSystemMetrics(1) - 30

    def show_image_beds(self):
        conf: Dict[str, Union[str, int]] = read_config(CONF_FILE)
        selected = conf.get("image_bed", None)
        if type(selected) == int:
            if selected >= 0:  # type: ignore
                self.image_bed = IMAGE_BEDS[selected]()  # type: ignore
                self.image_bed.auto_compress = self.auto_compress
        response = {
            "selected": selected,
            "beds": IMAGE_BEDS_CODE,
            "auth_data": conf.get("auth_data", None),
            "screensize": {"height": self.height, "width": self.width},
        }
        return response

    def init_image_bed(self, info: Dict[str, Union[str, int]]):
        # TODO: 如果有异常，返回false和错误详情
        img_bed_code = info["image-bed"]

        assert isinstance(img_bed_code, int)

        choose_image_bed(img_bed_code)
        self.image_bed = IMAGE_BEDS[img_bed_code]()

        # TODO: 判断条件需要修改为根据图床类型执行
        if img_bed_code == SM_MS:
            if not self.image_bed.login(info["username"], info["password"]):
                return {"success": False, "error": "用户名或密码错误"}
        elif img_bed_code == IMGTU:
            if not self.image_bed.login(info["username"], info["password"]):
                return {"success": False, "error": "用户名或密码错误"}
        elif img_bed_code == GITEE:
            self.image_bed.login(
                info["token"], info["username"], info["repo"], info["folder"]
            )
        elif img_bed_code == GITHUB:
            self.image_bed.login(
                info["token"], info["username"], info["repo"], info["folder"]
            )
        else:
            return {"success": False, "error": "未知的图床代码: %d" % img_bed_code}
        return {"success": True, "error": ""}

    def choose_image_bed(self, img_bed_code: int):
        # TODO: 选择图床后，应该将图床对应的认证信息保存到webview窗口，方便直接用窗口上传图片到网站
        choose_image_bed(img_bed_code)
        response = {"success": True}
        return response

    def upload_images(self):
        file_types = ("选择要上传的图片 (*.jpg;*.gif;*.png;*.jpeg)",)
        image_paths = webview.windows[0].create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
        )
        if image_paths and len(image_paths) > 10:
            response = {
                "success": False,
                "error": "一次最多只能上传 10 张图片，你上传了 %d 张" % len(image_paths),
            }
            return response
        urls = []
        if image_paths:
            try:
                urls = self.image_bed.upload_images(image_paths)  # type: ignore
            except OverSizeError as e:
                return {"success": False, "error": f"图片超限了 - {e}"}
            except UploadFailed as e:
                return {"success": False, "error": f"图床返回错误 - {e}"}

        response = {"success": True, "image_urls": urls}
        return response

    def toggle_automatic_compression(self, ac: bool):
        # TODO: 因为自动压缩功能不完善，所以默认是关闭的，每次启动程序都需要手动开启
        self.auto_compress = ac
        if self.image_bed:
            self.image_bed.auto_compress = self.auto_compress
        response = {"success": True, "automatic_compression": self.auto_compress}
        return response

    def automatic_compression_status(self):
        return {"automatic_compression": self.auto_compress}

    def get_all_images(self):
        if self.image_bed:
            images = self.image_bed.get_all_images()
        else:
            images = []
        response = {"success": True, "images": images}
        return response

    def view_image_in_new_windows(self, url: str, width: int, height: int):
        image_name = os.path.basename(url)
        # TODO: 根据当前屏幕尺寸显示大图
        if IS_WINDOWS:
            width = self.width if width + 20 > self.width else width + 38
            height = self.height if height + 20 > self.height else height + 72
        else:
            width = width + 20
            height = height + 20
        webview.create_window(
            image_name,
            html="<img src='%s'></img>" % url,
            width=width,
            height=height,
            resizable=False,
        )

    def delete_image(self, *args):
        result = self.image_bed.delete_image(*args)  # type: ignore

        if (
            isinstance(self.image_bed, SM)
            or isinstance(self.image_bed, Gitee)
            or isinstance(self.image_bed, Github)
        ):
            return {"success": result}
        elif isinstance(self.image_bed, Imgtu):
            status_code = result["status_code"]
            success = status_code == 200
            if success:
                return {"success": success}
            error = result["error"]["message"]
            response = {"success": success, "error": error}
            return response
        else:
            return {"success": False, "error": "未知的图床"}
