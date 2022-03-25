#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: types.py
# @Created:   2022-03-20 20:18:50
# @Modified:  2022-03-25 11:53:58


from collections import namedtuple

SMMS_DELETE_PARAMS = namedtuple("SMMS_DELETE_PARAMS", ["delete_url"])
IMGTU_DELETE_PARAMS = namedtuple("IMGTU_DELETE_PARAMS", ["id"])
GIT_DELETE_PARAMS = namedtuple("GIT_DELETE_PARAMS", ["sha", "delete_url"])
