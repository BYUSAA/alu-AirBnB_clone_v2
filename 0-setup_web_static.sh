#!/usr/bin/env bash
# This is a bash script for setting up a basic web static environment for development.

# Updating and upgrading the system to ensure all packages are up to date.
sudo apt-get -y update
sudo apt-get -y upgrade

# Installing Nginx, the web server, to serve our static content.
sudo apt-get -y install nginx

# Creating directories for the web static files: 'releases/test' will hold the versioned files,
# and 'shared' is for files that may be used across releases.
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Creating a simple test HTML file in the 'test' directory.
echo "Hello, this is a test HTML file." | sudo tee /data/web_static/releases/test/index.html

# Adding a new configuration: creating an HTML file for AirBnB clone with header and footer
# that will be displayed at /hbnb_static/0-index.html.
echo "<!DOCTYPE html>
<html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\" />
        <title>AirBnB clone</title>
    </head>
    <body style=\"margin: 0px; padding: 0px;\">
        <header style=\"height: 70px; width: 100%; background-color: #FF0000\">
        </header>

        <footer style=\"position: absolute; left: 0; bottom: 0; height: 60px; width: 100%; background-color: #00FF00; text-align: center; overflow: hidden;\">
            <p style=\"line-height: 60px; margin: 0px;\">Holberton School</p>
        </footer>
    </body>
</html>" | sudo tee /data/web_static/releases/test/0-index.html
# End of the new configuration file.

# Removing any existing symbolic link to 'current' and recreating it to point to the 'test' release.
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Changing ownership of the '/data' directory to the user 'ubuntu', so they have full access.
sudo chown -R ubuntu:ubuntu /data/

# Editing the Nginx default configuration file to add a new location block for '/hbnb_static'.
# This makes the '/hbnb_static' URL serve content from '/data/web_static/current'.
sudo sed -i '44i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restarting the Nginx service to apply the new configuration.
sudo service nginx restart
