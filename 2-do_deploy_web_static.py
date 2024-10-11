#!/usr/bin/python3
"""Deploy static content"""
from fabric.api import *
import os
import re
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ['3.80.74.138', '3.88.68.105']

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    local("mkdir -p versions")
    result = local("tar -cvzf versions/web_static_{}.tgz web_static"
                   .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                   capture=True)
    if result.failed:
        return None
    return result

def check_server_status():
    """Check if the deployed page is accessible"""
    for host in env.hosts:
        result = run(f"curl -s -o /dev/null -w '%{{http_code}}' http://{host}/hbnb_static/0-index.html")
        if result != "200":
            print(f"Error: Expected HTTP 200 but got {result} on host {host}")
            return False
    return True

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.isfile(archive_path):
        return False

    filename_regex = re.compile(r'[^/]+(?=\.tgz$)')
    match = filename_regex.search(archive_path)

    # Upload the archive to the /tmp/ directory of the web server
    archive_filename = match.group(0)
    result = put(archive_path, "/tmp/{}.tgz".format(archive_filename))
    if result.failed:
        return False

    # Uncompress the archive to the folder
    # /data/web_static/releases/<archive filename without extension> on
    # the web server
    result = run("mkdir -p /data/web_static/releases/{}/".format(archive_filename))
    if result.failed:
        return False
    result = run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
                 .format(archive_filename, archive_filename))
    if result.failed:
        return False

    # Delete the archive from the web server
    result = run("rm /tmp/{}.tgz".format(archive_filename))
    if result.failed:
        return False

    # Move content from web_static to release directory
    result = run("mv /data/web_static/releases/{}/web_static/* "
                 "/data/web_static/releases/{}/".format(archive_filename, archive_filename))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/releases/{}/web_static"
                 .format(archive_filename))
    if result.failed:
        return False

    # Delete the symbolic link /data/web_static/current from the web server
    result = run("rm -rf /data/web_static/current")
    if result.failed:
        return False

    # Create a new symbolic link pointing to the new release
    result = run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
                 .format(archive_filename))
    if result.failed:
        return False

    # Verify that the deployment was successful by checking HTTP status
    if not check_server_status():
        return False

    return True

