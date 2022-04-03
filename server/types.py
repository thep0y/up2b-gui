#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: types.py
# @Created:   2022-03-20 20:18:50
# @Modified:  2022-04-03 15:48:57


from collections import namedtuple
from typing import Union
from up2b.up2b_lib.up2b_api.coding import Coding
from up2b.up2b_lib.up2b_api.github import Github
from up2b.up2b_lib.up2b_api.imgtu import Imgtu
from up2b.up2b_lib.up2b_api.sm import SM

SMMS_DELETE_PARAMS = namedtuple("SMMS_DELETE_PARAMS", ["delete_url"])
IMGTU_DELETE_PARAMS = namedtuple("IMGTU_DELETE_PARAMS", ["id"])
GIT_DELETE_PARAMS = namedtuple("GIT_DELETE_PARAMS", ["sha", "delete_url"])
CODING_DELETE_PARAMS = namedtuple("GIT_DELETE_PARAMS", ["filename"])
ImageBedInstance = Union[Imgtu, SM, Github, Coding]
