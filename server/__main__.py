#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: __main__.py
# @Created:   2022-03-19 11:16:03
# @Modified:  2022-03-19 13:58:10

from server import app


def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    return resp


app.after_request(cors)
app.config["ENV"] = "development"
app.run(port=5000, debug=True)
