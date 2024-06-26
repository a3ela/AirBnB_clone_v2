#!/usr/bin/env bash
# Sets up web servers for deployment of web_static
sudo apt-get -y update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data
sudo sed -i "26i \ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}" /etc/nginx/sites-available/default
sudo service nginx reload
sudo service nginx restart
