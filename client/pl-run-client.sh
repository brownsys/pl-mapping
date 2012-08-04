#!/bin/bash

client_script="$1"

if [ ! -f "$client_script" ]; then
    echo "Invalid path to client script: $client_script"
    exit
fi

script_name=`basename $client_script`
running=`ps ax | pgrep $script_name`

if [ "$running" != "" ]; then
    exit
fi

echo "Scheduling client to run..."

# Run via cron so that it detaches easily

sudo /sbin/chkconfig crond on

cron_time=`date -v+2M +"%M %H %d %m *"`
echo "$cron_time $client_script" | crontab
