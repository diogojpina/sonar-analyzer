#!/bin/bash
sleep $[ ( $RANDOM % 10 )  + 1 ]s
cd /home/diogo/technicaldebt/sonar/docker/tcc-sonar
python3 -m auto_sonar -p /home/diogo/technicaldebt/git
