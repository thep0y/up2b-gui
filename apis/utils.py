#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: utils.py
# @Created:  2021-02-19 18:11:34
# @Modified: 2021-07-25 23:21:58

import json


def read_config(conf_path: str) -> dict:
    try:
        with open(conf_path, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        with open(conf_path, "w", encoding="utf-8") as f:
            f.write("{}")
            return {}
