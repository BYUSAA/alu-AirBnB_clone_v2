#!/usr/bin/python3
from fabric.api import env, run, put, local
from os.path import exists
from datetime import datetime


env.hosts = ['xx-web-01', 'xx-web-02']  # Replace with your actual server IPs


def do_pack():
    """Generates a .tgz archive from the web_static folder"""
    try:
        local("mkdir -p versions")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to /tmp/ directory
        put(archive_path, "/tmp/{}".format(file_name))

        # Create the release folder
        run("mkdir -p {}{}/".format(path, no_ext))

        # Uncompress the archive to the folder
        run("tar -xzf /tmp/{} -C {}{}/".format(file_name, path, no_ext))

        # Delete the archive from /tmp/
        run("rm /tmp/{}".format(file_name))

        # Move the content out of the web_static folder
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, no_ext))

        # Remove the empty web_static folder
        run("rm -rf {}{}/web_static".format(path, no_ext))

        # Delete the symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {}{}/ /data/web_static/current".format(path, no_ext))

        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
