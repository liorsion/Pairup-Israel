#!/bin/bash
echo "collecting static files"
cd ~/Documents/workspace/find-a-partner/findapartner/
./manage.py collectstatic

echo "compressing common.css"
java -jar /Applications/yuicompressor-2.4.6/build/yuicompressor-2.4.6.jar /Users/liorsion/Documents/workspace/find-a-partner/static_root/css/common.css -o /Users/liorsion/Documents/workspace/find-a-partner/static_root/css/common.css

echo "compressing tagsinput css"
java -jar /Applications/yuicompressor-2.4.6/build/yuicompressor-2.4.6.jar /Users/liorsion/Documents/workspace/find-a-partner/static_root/css/jquery.tagsinput.css -o /Users/liorsion/Documents/workspace/find-a-partner/static_root/css/jquery.tagsinput.css 



