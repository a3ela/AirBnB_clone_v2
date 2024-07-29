#!/usr/bin/python3

"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers,
using the function do_deploy
"""
from fabric.api import *
from fabric.operations import run, put
import os
import time


env.hosts = ['54.237.48.16', '18.234.145.133']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """generates a .tgz archive"""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{:s}.tgz web_static/".
              format(time.strftime("%Y%m%d%H%M%S")))
        return "versions/web_static_{:s}.tgz".\
            format(time.strftime("%Y%m%d%H%M%S"))
    except BaseException:
        return None


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
    except BaseException:
        return False

    return True


def deploy():
    """
    creates and distributes an archive to my web servers
    """
    created_archive = do_pack()
    if not created_archive:
        return False
    return do_deploy(created_archive)
