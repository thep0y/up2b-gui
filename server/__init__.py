#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: __init__.py
# @Created:   2022-03-17 11:44:25
# @Modified:  2022-04-03 18:12:22

from flask import Flask, jsonify, send_from_directory, request
from up2b.up2b_lib.custom_types import ErrorResponse, ImageStream
from up2b.up2b_lib.up2b_api.coding import Coding
from up2b.up2b_lib.up2b_api.imgtu import Imgtu
from up2b.up2b_lib.up2b_api.sm import SM
from server.consts import ASSETS_DIR, CONNECT_ERROR, GET, INDEX_PATH, POST, STATIC_DIR
from server.apis import Api
from server.types import (
    CODING_DELETE_PARAMS,
    GIT_DELETE_PARAMS,
    IMGTU_DELETE_PARAMS,
    SMMS_DELETE_PARAMS,
)

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/assets")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
api = Api()


@app.route("/", methods=[GET])
def index():
    with open(INDEX_PATH) as f:
        return f.read()


@app.route("/favicon.ico", methods=[GET])
def favicon():
    return send_from_directory(
        ASSETS_DIR,
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/getImageBeds")
def get_image_beds():
    return jsonify(api.show_image_beds())


@app.route("/chooseImageBed/<int:code>")
def choose_image_bed(code: int):
    return jsonify(api.choose_image_bed(code))


@app.route("/init", methods=[POST])
def init_image_bed():
    data = request.get_json()
    result = api.init_image_bed(data)
    if not result["success"]:
        api.image_bed_code = None

    return jsonify(result)


@app.route("/ac/<int:status>", methods=[GET])
def toggle_automatic_compression(status: int):
    return jsonify(api.toggle_automatic_compression(status == 1))


@app.route("/upload", methods=[POST])
def upload():
    if "file" not in request.files:
        return jsonify(success=False)

    file = request.files["file"]

    assert file.filename is not None

    if not api.image_bed:
        return jsonify(success=False, error="尚未配置或选择图床"), 401

    print("上传 ->", file.filename)

    stream = ImageStream(file.filename, file.stream.read(), file.mimetype)

    try:
        result = api.image_bed.upload_image_stream(stream)
        print("上传结束 ->", file.filename, result)
    except ConnectionError:
        return jsonify(success=False, error=CONNECT_ERROR)
    else:
        if isinstance(result, str):
            return jsonify(success=True, url=result)

        return jsonify(success=False, error=result.to_dict())


@app.route("/getAllImages", methods=[GET])
def get_all_images():
    images = api.get_all_images()
    if images is None:
        return jsonify(success=False, error="尚未配置或选择图床")

    if isinstance(images, ErrorResponse):
        return jsonify(success=False, error=images.to_dict())

    return jsonify(success=True, image_code=api.image_bed_code, urls=images)


@app.route("/preview", methods=[POST])
def preview():
    data = request.get_json()

    assert data is not None

    if app.config["ENV"] != "development":
        api.view_image_in_new_windows(data["url"], data["width"], data["height"])
        return jsonify(success=True)

    return jsonify(success=False, error="当前为开发环境，无法打开新窗口，用打开一个新的浏览器标签页替代")


@app.route("/delete", methods=[POST])
def delete():
    data = request.get_json()

    assert data is not None

    if isinstance(api.image_bed, SM):
        params = SMMS_DELETE_PARAMS(data["delete_url"])
    elif isinstance(api.image_bed, Imgtu):
        params = IMGTU_DELETE_PARAMS(data["id"])
    elif isinstance(api.image_bed, Coding):
        params = CODING_DELETE_PARAMS(data["filename"])
    else:
        params = GIT_DELETE_PARAMS(data["sha"], data["delete_url"])

    try:
        result = api.delete_image(params)
    except ConnectionError:
        return jsonify(success=False, error=CONNECT_ERROR)

    return jsonify(result)
