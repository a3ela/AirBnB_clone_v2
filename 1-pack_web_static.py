#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from contents
of the web_static folder.
name of the archive created must be
web_static_<year><month><day><hour><minute><second>.tgz
Otherwise, it should return None
"""
from fabric.api import local
import time


def do_pack():
    """generates a .tgz archive"""
    try:
        local('mkdir -p versions')
        local('tar -cvzf versions/web_static_{:s}.tgz web_static/'.
              format(time.strftime('%Y%m%d%H%M%S')))
        return 'versions/web_static_{:s}.tgz'.\
               format(time.strftime('%Y%m%d%H%M%S'))
    except BaseException:
        return None
