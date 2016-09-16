#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import logging
from transwarp.web import get, view
from models import User, Blog, Comment

@view('test_users.html')     # @view指定模板文件
@get('/')
def test_user():
    users = User.find_all()
    return dict(users=users)
