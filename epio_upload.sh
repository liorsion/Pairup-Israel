#!/bin/bash
./prepare_upload.sh

cd ~/Documents/workspace/find-a-partner/
epio upload
epio django syncdb
epio django migrate
