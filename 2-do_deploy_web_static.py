#!/usr/bin/python3
from fabric.api import env, run, put, local
from os.path import exists
from datetime import datetime

env.hosts = ['xx-web-01', 'xx-web-02']  # Replace with your actual web server IPs


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
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

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))

        # Uncompress the archive to the folder /data/web_static/releases/<archive_name>
        run("mkdir -p {}{}/".format(path, no_ext))
        run("tar -xzf /tmp/{} -C {}{}/".format(file_name, path, no_ext))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))

        # Move the contents of the web_static folder to the correct directory
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, no_ext))
        run("rm -rf {}{}/web_static".format(path, no_ext))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current linked to the new version
        run("ln -s {}{}/ /data/web_static/current".format(path, no_ext))
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

