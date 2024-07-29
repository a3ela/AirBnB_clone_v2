#!/usr/bin/env python3

""" Fabric script that generates a .tgz 
archive from the contents of the web_static 
folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    time = datetime.now()
    str_time = time.strftime('%Y%m%d%H%M%S')
    file_path = f'versions/web_static_{str_time}.tgz'
    file_size = os.path.getsize(file_path)

    local('sudo mkdir -p versions')
    local("sudo tar -cvzf versions/web_static_{str_time}.tgz web_static")
    print(f'web_static packed: versions/web_static_{str_time}.tgz -> {file_size}Bytes')
