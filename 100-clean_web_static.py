#!/usr/bin/python3
"""
do_clean: cleans old archives from the version dir on the servers provided
Usage:
    fab -f 100-clean_web_static.py do=clean:number=2
    optional: -i sshkey -u ubuntu
"""
import fabric.api import *
import os

env.hosts = ['54.237.48.16', '18.234.145.133']
env.user = "ubuntu"


def do_clean(number=0):
    """ Delete out dated archives
    args:
    number: the number of archives to keep while
    deleting the rest
    """
    # local versions dir cleanup
    run(f"ls -ltr versions | sort -nr | tail -n +{number + 1} | xargs rm -f")

    # remote versions dir cleanup on servers
    remote_versions_dir = "/data/web_static/releases/"
    sudo(f"ls -ltr {remote_versions_dir} | sort -nr | \
        tail -n +{number + 1} | xargs rm -f")
