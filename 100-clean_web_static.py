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
    """ Delete out dated archives
    args:
    number: the number of archives to keep while
    deleting the rest
    """
    number = int(number)
    local_dir = "versions"
    run(f"find {local_dir} -type f -name '*.tar.gz' | sort -nr | tail -n +{int(number + 1)} | xargs rm -f")

      # Remote versions folder cleanup (on both web servers)
    remote_dir = "/data/web_static/releases"
    sudo(f"find {remote_dir} -type f -name '*.tar.gz' | sort -nr | tail -n +{int(number + 1)} | xargs rm -f")
