#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers.
"""

from fabric.api import env, put, run
from os.path import exists

# Define the web servers and the SSH connection details
env.hosts = ['54.242.133.62', '34.233.128.212']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"  # Corrected from env.key to env.key_filename

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): The path to the archive file to be deployed.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """
    # Check if the specified archive exists before proceeding
    if not exists(archive_path):
        return False

    try:
        # Extract the file name from the archive path
        file_name = archive_path.split("/")[-1]

        # Extract the base name (without extension) for creating deployment paths
        name = file_name.split(".")[0]

        # Define the path where the archive will be unpacked
        path_name = "/data/web_static/releases/" + name

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Create the release directory on the server
        run("mkdir -p {}/".format(path_name))

        # Unpack the archive in the release directory
        run("tar -xzf /tmp/{} -C {}/".format(file_name, path_name))

        # Remove the uploaded archive from the /tmp/ directory
        run("rm /tmp/{}".format(file_name))

        # Move the contents from web_static folder to the release directory
        run("mv {}/web_static/* {}".format(path_name, path_name))

        # Remove the now-empty web_static directory
        run("rm -rf {}/web_static".format(path_name))

        # Remove the existing symbolic link to current version
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link pointing to the new release
        run("ln -s {}/ /data/web_static/current".format(path_name))

        # Return True to indicate the deployment was successful
        return True
    except Exception:
        # In case of an error, return False to indicate failure
        return False
