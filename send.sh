#! /bin/bash

ip="188.166.167.45"
port="22"

scp -P $port ./p_pyless.tgz debian@$ip:project/
scp -P $port ./deploy.sh debian@$ip:project/
