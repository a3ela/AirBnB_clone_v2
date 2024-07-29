#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes an archive to your web servers, using the function do_deploy:
Prototype: def do_deploy(archive_path):
Returns False if the file at the path archive_path doesn’t exist
"""
from fabric.api import *
import time
import os
from fabric.operations import run, put

env.hosts = ['54.237.48.16', '18.234.145.133']


def do_pack():
    """create a tgz archive"""
    try:
        local('mkdir -p versions')
        local('tar -cvzf versions/web_static_{:s}.tgz web_static/'.
                format(time.strftime('%Y%m%d%H%M%S')))
        return 'versions/web_static_{:s}.tgz'.\
                format(time.strftime('%Y%m%d%H%M%S'))
    except BaseException:
        return None

def do_deploy(archive_path):
    """""deploy you codebase"""
    t_str = time.strftime('%Y%m%d%H%M%S')

    if not os.path.exists(archive_path):
        return False
    try:
        # upload the archive to /tmp of the wen server
        put(archive_path, '/tmp/')
        #create a file with the time stamp
        run('sudo mkdir -p /data/web_static/releases/web_static_{:s}/'.
                format(t_str))
        
        # uncomprestion
        run('sudo tar -xzf /tmp/web_static_{:s}.tgz -C /data/web_static/releases/web_static_{:s}/'.format(t_str, t_str))

        # delete the archive
        run('sudo rm /tmp/web_static_{:s}'.format(t_str))

        # move contents into web_static
        run('sudo mv /data/web_static/releases/web_static_{:s}/web_static/*\
                /data/web_static/releases/web_static_{}'.format(t_str, t_str))

        # remove irrelevant web_static dir
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(t_str))

        # delete the symobolic link from the web server
        run('sudo rm -rf /data/web_static/current')

        # create a new stybolic link
        run('sudo ln -s /data/web_static/releases/web_static_{:s}/ \
                /data/web_static/current'.format(t_str))
    except BaseException:
        return False

    return True

















