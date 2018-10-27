#!/bin/bash

wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
gunzip GeoLiteCity.dat.gz
mkdir -p ~/hive5/location/db
mv GeoLiteCity.dat ~/hive5/location/db
