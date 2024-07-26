#!/usr/bin/env bash
# script that sets up web servers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx

mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

touch /data/web_static/releases/test/index.html

echo "<html>
	<head>
	</head>
	<body>
		Holberton School
	</body>
</html>" | tee /data/web_static/releases/test/index.html > /dev/null

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R "$USER": /data/

sudo nginx_config="/etc/nginx/sites-available/default"
if [ -e "$nginx_config" ]; then
		sudo sed -i '/server_name_;/a \\n   location /hbnb_static/ {\n      alias /data/web_static/current/;\n   }\n' "$nginx_config"
fi

sudo service nginx restart
