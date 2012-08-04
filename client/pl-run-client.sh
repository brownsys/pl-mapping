#!/bin/bash

client_script="$1"

if [ ! -f "$client_script" ]; then
    echo "Invalid path to client script: $client_script"
    exit
fi

script_name=`basename $client_script`
running=`pgrep -fl $script_name | grep -v $0`

if [ "$running" != "" ]; then
    echo "Client is already running."
    exit
fi

echo "Scheduling client to run..."

# Run via cron so that it detaches easily

sudo /etc/init.d/crond start

cron_time=`date --date="+2min" +"%M %H %d %m *"`
echo "$cron_time $client_script" | crontab
