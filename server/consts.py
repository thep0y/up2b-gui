#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: consts.py
# @Created:   2022-03-17 12:05:50
# @Modified:  2022-03-31 12:10:17

import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
INDEX_PATH = os.path.join(ASSETS_DIR, "index.html")
STATIC_DIR = os.path.join(ASSETS_DIR, "assets")

POST = "POST"
GET = "GET"


CONNECT_ERROR = "网络异常"
