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

    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
