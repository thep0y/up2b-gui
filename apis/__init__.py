#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@aliyun.com
# @File Name: __init__.py
# @Created: 2021-02-19 16:42:55
# @Modified: 2021-02-25 10:43:39

import sys
import webview

from typing import Dict
from timg import IMAGE_BEDS
from timg.timglib.timg_api import CONF_FILE, choose_image_bed
from timg.timglib.timg_api.sm import SM
from timg.timglib.timg_api.imgtu import Imgtu
from timg.timglib.timg_api.gitee import Gitee
from timg.timglib.timg_api.github import Github
from timg.timglib.constants import IMAGE_BEDS_CODE, SM_MS, IMGTU, GITEE, GITHUB
from apis.utils import read_config
from apis.errors import InvalidImageBedCode


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False
        self.image_bed = None
        self.auto_compress: bool = False
        # self.conf: Dict[str, str] = read_config(CONF_FILE)

    def show_image_beds(self):
        conf = read_config(CONF_FILE)
        selected = conf.get("image_bed", None)
        if selected >= 0:
            self.image_bed = IMAGE_BEDS[selected]()
            self.image_bed.auto_compress = self.auto_compress
        response = {
            "selected": selected,
            "beds": IMAGE_BEDS_CODE,
            "auth_data": conf.get("auth_data", None)
        }
        return response

    def init_image_bed(self, info: Dict[str, str]):
        # TODO: 如果有异常，返回false和错误详情
        img_bed_code = int(info["image-bed"])
        choose_image_bed(img_bed_code)
        self.image_bed = IMAGE_BEDS[img_bed_code]()
        if img_bed_code == SM_MS:
            self.image_bed.login(info["username"], info["password"])
        elif img_bed_code == IMGTU:
            self.image_bed.login(info["username"], info["password"])
        elif img_bed_code == GITEE:
            self.image_bed.login(info["access-token"], info["username"],
                                 info["repository"], info["path"])
        elif img_bed_code == GITHUB:
            self.image_bed.login(info["access-token"], info["username"],
                                 info["repository"], info["path"])
        else:
            raise InvalidImageBedCode("未知的图床代码")
        # 如果程序有异常，此处会退出，没有退出就是正常登录
        response = {"success": True}
        return response

    def choose_image_bed(self, img_bed_code: int):
        # TODO: 选择图床后，应该将图床对应的认证信息保存到webview窗口，方便直接用窗口上传图片到网站
        choose_image_bed(img_bed_code)
        response = {"success": True}
        return response

    def upload_images(self):
        file_types = ('选择要上传的图片 (*.jpg;*.gif;*.png;*.jpeg)', )
        image_paths = webview.windows[0].create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
        if image_paths and len(image_paths) > 10:
            response = {
                "success": False,
                "error": "一次最多只能上传 10 张图片，你上传了 %d 张" % len(image_paths)
            }
            return response
        urls = []
        if image_paths:
            urls = self.image_bed.upload_images(image_paths)
        response = {"success": True, "image_urls": urls}
        return response

    def toggle_automatic_compression(self, ac: bool):
        # TODO: 因为自动压缩功能不完善，所以默认是关闭的，每次启动程序都需要手动开启
        self.auto_compress = ac
        if self.image_bed:
            self.image_bed.auto_compress = self.auto_compress
        response = {
            "success": True,
            "automatic_compression": self.auto_compress
        }
        return response

    def automatic_compression_status(self):
        return {"automatic_compression": self.auto_compress}

    def get_all_images(self):
        if self.image_bed:
            images = self.image_bed.get_all_images()
        else:
            images = []
        response = {
            "success": True,
            "images": images,
        }
        return response

    def view_image_in_new_windows(self, url: str, width: int, height: int):
        is_windows = sys.platform == "win32"
        webview.create_window(
            "查看图片",
            html="<img src='%s'></img>" % url,
            width=width + 30 if is_windows else width + 20,
            height=height + 72 if is_windows else height + 20,
        )

    def delete_image(self, *args):
        result = self.image_bed.delete_image(*args)

        if isinstance(self.image_bed, SM) or isinstance(
                self.image_bed, Gitee) or isinstance(self.image_bed, Github):
            return {"success": result}
        elif isinstance(self.image_bed, Imgtu):
            status_code = result["status_code"]
            success = status_code == 200
            if success:
                return {"success": success}
            error = result["error"]["message"]
            response = {
                "success": success,
                "error": error,
            }
            return response
        else:
            return {"success": False, "error": "未知的图床"}
