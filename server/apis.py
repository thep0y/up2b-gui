#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: apis.py
# @Created:   2022-03-17 12:57:02
# @Modified:  2022-04-03 16:14:19

import os
from up2b.up2b_lib.custom_types import AuthData, ErrorResponse
from up2b.up2b_lib.up2b_api.coding import Coding
import webview

from typing import Dict, Optional, Union
from requests.exceptions import ConnectionError
from up2b import IMAGE_BEDS
from up2b.up2b_lib.up2b_api import GitBase, choose_image_bed
from up2b.up2b_lib.up2b_api.sm import SM
from up2b.up2b_lib.up2b_api.imgtu import Imgtu
from up2b.up2b_lib.constants import (
    CONF_FILE,
    ImageBedCode,
    IS_WINDOWS,
)
from up2b.up2b_lib.errors import OverSizeError, UploadFailed
from server.consts import CONNECT_ERROR
from server.utils import read_config
from server.types import (
    GIT_DELETE_PARAMS,
    IMGTU_DELETE_PARAMS,
    SMMS_DELETE_PARAMS,
    CODING_DELETE_PARAMS,
    ImageBedInstance,
)

if IS_WINDOWS:
    import ctypes


class Api:
    image_bed_code: Optional[ImageBedCode]

    def __init__(self):
        self.cancel_heavy_stuff_flag = False
        self.auto_compress: bool = False
        self.height = self.width = 0
        if IS_WINDOWS:
            user32 = ctypes.windll.user32
            self.width: int = user32.GetSystemMetrics(0)
            self.height: int = user32.GetSystemMetrics(1) - 30
        self.conf: Dict[str, Union[AuthData, int]] = read_config(CONF_FILE)

        selected = self.conf.get("image_bed", -1)

        assert isinstance(selected, int)

        self.image_bed_code = ImageBedCode(selected) if selected >= 0 else None

    @property
    def image_bed(self) -> Optional[ImageBedInstance]:
        if self.image_bed_code is None:
            return None

        image_bed = IMAGE_BEDS[self.image_bed_code]()
        image_bed.auto_compress = self.auto_compress
        return image_bed

    def show_image_beds(self):
        auth_data = self.conf.get("auth_data", {})
        assert isinstance(auth_data, dict)

        response = {
            "selected": self.image_bed_code.value
            if self.image_bed_code is not None
            else None,
            "save_beds": [int(i) for i in auth_data.keys()],
            "types": [i().image_bed_type.value for i in IMAGE_BEDS.values()],
            "screensize": {"height": self.height, "width": self.width},
        }
        return response

    def init_image_bed(self, info: Dict[str, Union[str, int]]):
        img_bed_code = info["image-bed"]

        assert isinstance(img_bed_code, int)

        self.image_bed_code = ImageBedCode(img_bed_code)

        # TODO: 判断条件需要修改为根据图床类型执行
        if self.image_bed_code == ImageBedCode.SM_MS:
            assert isinstance(self.image_bed, SM)
            if not self.image_bed.login(info["username"], info["password"]):  # type: ignore
                return {"success": False, "error": "用户名或密码错误"}
        elif self.image_bed_code == ImageBedCode.IMGTU:
            assert isinstance(self.image_bed, Imgtu)
            if not self.image_bed.login(info["username"], info["password"]):  # type: ignore
                return {"success": False, "error": "用户名或密码错误"}
        elif self.image_bed_code == ImageBedCode.GITHUB:
            assert isinstance(self.image_bed, GitBase)
            self.image_bed.login(
                info["token"], info["username"], info["repo"], info["folder"]  # type: ignore
            )
        elif self.image_bed_code == ImageBedCode.CODING:
            assert isinstance(self.image_bed, Coding)
            self.image_bed.login(
                info["token"], info["username"], info["project"], info["repo"], info["folder"]  # type: ignore
            )
        else:
            return {"success": False, "error": "未知的图床代码: %d" % img_bed_code}

        # 认证信息保存成功后才切换图床
        choose_image_bed(img_bed_code)

        return {"success": True, "error": ""}

    def choose_image_bed(self, img_bed_code: int):
        try:
            choose_image_bed(img_bed_code)
            self.image_bed_code = ImageBedCode(img_bed_code)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": e.args[0]}

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
                assert self.image_bed is not None
                urls = self.image_bed.upload_images(image_paths)
            except OverSizeError as e:
                return {"success": False, "error": f"图片超限了 - {e}"}
            except UploadFailed as e:
                return {"success": False, "error": f"图床返回错误 - {e}"}

        response = {"success": True, "image_urls": urls}
        return response

    def toggle_automatic_compression(self, ac: bool):
        # 因为自动压缩功能不完善，所以默认是关闭的，每次启动程序都需要手动开启
        if self.image_bed_code == -1:
            return {"success": False, "error": "尚未配置或选择图床"}

        self.auto_compress = ac
        response = {"success": True, "status": ac}
        return response

    def automatic_compression_status(self):
        return {"automatic_compression": self.auto_compress}

    def get_all_images(self):
        if self.image_bed:
            try:
                images = self.image_bed.get_all_images()
                return images
            except ConnectionError:
                return ErrorResponse(status_code=500, error=CONNECT_ERROR)

    def view_image_in_new_windows(self, url: str, width: int, height: int):
        image_name = os.path.basename(url)

        width_delta = 28 if IS_WINDOWS else 20
        height_delta = 61 if IS_WINDOWS else 20

        max_width = 1920 - 34
        max_height = 1080 - 67

        # 最大窗口尺寸 1920x1080
        if width > max_width:
            height = int(float(height) * (max_width / width))
            width = max_width

        if height > max_height:
            width = int(float(width) * (max_height / height))
            height = max_height

        webview.create_window(
            image_name,
            html=f"<img src='{url}' width='{width}' height='{height}'></img>",
            width=width + width_delta,
            height=height + height_delta,
            resizable=False,
        )

    def delete_image(
        self,
        params: Union[
            SMMS_DELETE_PARAMS,
            IMGTU_DELETE_PARAMS,
            GIT_DELETE_PARAMS,
            CODING_DELETE_PARAMS,
        ],
    ):
        if isinstance(params, SMMS_DELETE_PARAMS):
            assert isinstance(self.image_bed, SM)
            result = self.image_bed.delete_image(params.delete_url)
        elif isinstance(params, IMGTU_DELETE_PARAMS):
            assert isinstance(self.image_bed, Imgtu)
            result = self.image_bed.delete_image(params.id)
        elif isinstance(params, CODING_DELETE_PARAMS):
            assert isinstance(self.image_bed, Coding)
            result = self.image_bed.delete_image(params.filename)
        else:
            assert isinstance(self.image_bed, GitBase)
            result = self.image_bed.delete_image(params.sha, params.delete_url)

        if not result:
            return {"success": True}

        if result.status_code == 400 and result.error == "图片已被删除，请耐心等待服务器刷新缓存":
            return {"success": True, "msg": result.error}

        return {"success": False, "error": result.to_dict()}
