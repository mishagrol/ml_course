#!/bin/bash
apt-get update
apt-get install nginx -y
service nginx start
sed -i --"s/nginx/Yandex Cloud - /" /var/www/html/index.nginx-debian.html
