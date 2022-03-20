#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: types.py
# @Created:   2022-03-20 20:18:50
# @Modified:  2022-03-20 21:47:15


from collections import namedtuple

SMMS_DELETE_PARAMS = namedtuple("smms_delete_params", ["delete_url"])
IMGTU_DELETE_PARAMS = namedtuple("imgtu_delete_params", ["id"])
GIT_DELETE_PARAMS = namedtuple("git_delete_params", ["sha", "delete_url"])
