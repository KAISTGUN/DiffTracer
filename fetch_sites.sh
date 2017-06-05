#!/bin/sh
wget https://s3.amazonaws.com/alexa-static/top-1m.csv.zip
unzip top-1m.csv.zip
rm -f top-1m.csv.zip
