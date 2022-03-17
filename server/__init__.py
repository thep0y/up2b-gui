#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: __init__.py
# @Created:   2022-03-17 11:44:25
# @Modified:  2022-03-17 20:56:11

from flask import Flask, jsonify, send_from_directory, request
from up2b.up2b_lib.custom_types import ImageStream
from server.consts import ASSETS_DIR, INDEX_PATH, STATIC_DIR
from server.apis import Api

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/assets")
api = Api()


@app.route("/")
async def index():
    with open(INDEX_PATH) as f:
        return f.read()


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(
        ASSETS_DIR,
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/getImageBeds")
async def get_image_beds():
    return jsonify(api.show_image_beds())


@app.route("/chooseImageBed/<int:code>")
async def choose_image_bed(code: int):
    return jsonify(api.choose_image_bed(code))


@app.route("/init", methods=["POST"])
async def init_image_bed():
    data = request.get_json()
    return jsonify(api.init_image_bed(data))


@app.route("/ac/<int:status>", methods=["GET"])
async def toggle_automatic_compression(status: int):
    return jsonify(api.toggle_automatic_compression(status == 1))


@app.route("/upload", methods=["POST"])
async def upload():
    if "file" not in request.files:
        return jsonify(success=False), 400

    file = request.files["file"]

    if not api.image_bed:
        return jsonify(success=False, error="没有配置正在使用的图床"), 403

    result = api.image_bed.upload_images(
        ImageStream(
            file.filename,  # type:ignore
            file.stream.read(),
            file.mimetype,
        ),
        to_console=False,
    )

    result = result[0]
    if isinstance(result, str):
        return jsonify(success=True, url=result), 200
    else:
        if result["error"] == "重复上传" and result["status_code"] == 400:
            return (
                jsonify(success=False, error="imgtu.com 暂时关闭了上传重复图片，且其未返回已上传图片的链接"),
                400,
            )
    return jsonify(success=False, error=result["error"]), result["status_code"]
