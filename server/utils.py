#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: utils.py
# @Created:   2022-03-17 12:08:30
# @Modified:  2022-03-18 08:11:22

import json


def read_config(conf_path: str) -> dict:
    try:
        with open(conf_path, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        with open(conf_path, "w", encoding="utf-8") as f:
            f.write("{}")
            return {}
