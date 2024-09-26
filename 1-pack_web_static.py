#!/usr/bin/python3
"""
Fabric script which generates a tgz archive of the web_static directory.
"""

from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """
    Creates a .tgz archive of the web_static directory.

    The archive will be saved in the 'versions' directory, and its name will 
    include a timestamp to ensure uniqueness. If the 'versions' directory does 
    not exist, it will be created.
    
    Returns:
        str: The path to the created archive, or None if the process fails.
    """
    try:
        # Generate a timestamp to append to the archive name
        date = datetime.now().strftime("%Y%m%d%H%M%S")

        # Check if the 'versions' directory exists, and create it if it doesn't
        if not isdir("versions"):
            local("mkdir versions")
        
        # Define the archive name with the generated timestamp
        file_name = "versions/web_static_{}.tgz".format(date)

        # Create the .tgz archive of the 'web_static' directory
        local("tar -cvzf {} web_static".format(file_name))

        # Return the file name of the created archive
        return file_name
    except Exception:
        # In case of an error, return None to indicate failure
        return None
