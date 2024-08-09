#!/usr/bin/python3
"""
do_clean: cleans old archives from the version dir on the servers provided
Usage:
    fab -f 100-clean_web_static.py do=clean:number=2
    optional: -i sshkey -u ubuntu
"""
from fabric.api import local, run, env, sudo

env.user = "ubuntu"
env.hosts = ["54.237.48.16", "18.234.145.133"]


def do_clean(number=0):
    """Deletes out-of-date archives"""
    files = local("ls -1t versions", capture=True)
    file_names = files.split("\n")
    n = int(number)
    if n in (0, 1):
        n = 1
    for i in file_names[n:]:
        local("rm versions/{}".format(i))
    dir_server = run("ls -1t /data/web_static/releases")
    dir_server_names = dir_server.split("\n")
    for i in dir_server_names[n:]:
        if i is 'test':
            continue
        run("rm -rf /data/web_static/releases/{}"
            .format(i))
