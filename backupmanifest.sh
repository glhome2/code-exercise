#!/bin/bash
xmlurl=$1
zipfile=$2

wget "$xmlurl"
mkdir project
cd project
repo init -u $xmlurl
repo sync
# zip project
cd ..
cp *.xml project/
zip -r $zipfile project
