#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to
your web servers, using the function do_deploy:
Prototype: def do_deploy(archive_path):
Returns False if the file at the path archive_path doesn’t exist
"""
from fabric.api import *
import time
import os
from fabric.operations import run, put

env.hosts = ['54.237.48.16', '18.234.145.133']


def do_deploy(archive_path):
    """""deploy you codebase"""
    t_str = time.strftime('%Y%m%d%H%M%S')
    f_name = archive_path.split('/')[-1]
    f_noext = f_name.split('.')[0]

    if not os.path.exists(archive_path):
        return False
    try:
        # upload the archive to tmp of the wen server
        put(archive_path, '/tmp/')

        # create a file with the time stamp
        run('sudo mkdir -p /data/web_static/releases/{}/'.
            format(f_noext))

        # uncomprestion
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.
            format(f_name, f_noext))

        # delete the archive
        run('sudo rm /tmp/{}'.format(f_name))

        # move contents into web_static
        run('sudo mv /data/web_static/releases/{}/web_static/*\
                /data/web_static/releases/{}'.format(f_noext, f_noext))

        # remove irrelevant web_static dir
        run('sudo rm -rf /data/web_static/releases/{}/web_static'.
            format(f_noext))

        # delete the symobolic link from the web server
        run('sudo rm -rf /data/web_static/current')

        # create a new stybolic link
        run('sudo ln -s /data/web_static/releases/{}/ \
                /data/web_static/current'.format(f_noext))

        print("New version deployed!")
    except BaseException:
        return False

    return True
