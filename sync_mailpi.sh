#!/bin/sh

rsync -vae 'ssh' --delete  _build/* bilder@192.168.1.13:/var/www/bilder
ssh bilder@192.168.1.13 'chmod a-w /var/www/bilder/* -R'
