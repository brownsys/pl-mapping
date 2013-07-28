#!/bin/bash

master_host="rest.cs.brown.edu"
upload_url="http://$master_host/pl-mapping/pl-upload.php"
get_work_url="http://$master_host/pl-mapping/pl-get-work.php"
worker_ping_url="http://$master_host/pl-mapping/pl-worker-ping.php"

sleep_bw_work_checks_min=600 # 10 minutes
sleep_bw_work_checks_max=1200 # 20 minutes
sleep_if_server_unresponsive=7200 # 2 hours
sleep_at_start_max=1200 # 20 minutes

output_prefix="rev-"
output_suffix=".txt"

function do_lookups {
	start_addr=$1
	mask=$2

	output="$output_prefix$start_addr-$mask$output_suffix"
	q1=`echo $start_addr | cut -d. -f 1`
	q2=`echo $start_addr | cut -d. -f 2`
	q3=`echo $start_addr | cut -d. -f 3`
	q4=`echo $start_addr | cut -d. -f 4`

	if [ "$mask" == "" ]; then return; fi
	if [ "`echo $start_addr | grep '\.'`" == "" ]; then return; fi
	if [ "$q4" == "" ]; then return; fi
	if [ "$mask" -gt 32 ]; then return; fi

	i=0
	max=$((2 ** $((32 - $mask))))

	while [ $i -lt $max ]; do
		a=$(($q1 + $(( $i / $((256 ** 3)) )) ))
		b=$(($q2 + $(( $i / $((256 ** 2)) )) ))
		c=$(($q3 + $(( $i / $((256 ** 1)) )) ))
		d=$(($q4 + $(( $i % 256 )) ))
		addr="$a.$b.$c.$d"
		
		host $addr >> $output
		sleep 1

		if [ $d -eq 255 ]; then
			curl -s "$worker_ping_url?start_addr=$start_addr&mask=$mask&last_addr=$addr&hostname=$HOSTNAME"
		fi

		i=$((i+1))
	done

	sleep 5 # sleep between 5 and 20 seconds
	sleep $(($RANDOM % 15))

	curl -s --upload-file "$output" "$upload_url?start_addr=$start_addr&mask=$mask&file=$output&hostname=$HOSTNAME"

	sleep 5
	rm $output
}

function get_work {
	response=`curl -s "$get_work_url?hostname=$HOSTNAME"`
	curl_success=$?
	res_check=`echo $response | cut -d: -f1`

	if [ "$curl_success" -gt 0 ]; then
		sleep $sleep_if_server_unresponsive
	elif [ "$res_check" == "MAPPING_COMMAND" ]; then
		cmd=`echo $response | cut -d: -f2`
		arg=`echo $response | cut -d: -f3`

		if [ "$cmd" != "sleep" ]; then
			do_lookups "$cmd" "$arg"
		else
			sleep $arg
		fi
	fi
}

function startup {
	# Ensure the host command is available

	if [ "`host $master_host`" == "" ]; then
		sudo yum -y install bind-utils
		sleep 30
		if [ "`host $master_host`" == "" ]; then
			sleep 270 # could have been a temporary failure
			sudo yum -y install bind-utils
			sleep 30
			if [ "`host $master_host`" == "" ]; then
				exit # assume permanant failure
			fi
		fi
	fi

	# Delete old outputs

	rm "$output_prefix"*"$output_suffix"

	# Set ourself to run after reboot

	echo "@reboot $0" | crontab
	sudo /sbin/chkconfig --add crond # Ensures crond runs at startup
	sudo /sbin/chkconfig crond on
}

startup

#  Sleep a random amount, not greater than twenty minutes
sleep $(($RANDOM % $sleep_at_start_max));

while true; do
	get_work

	incr=$(($sleep_bw_work_checks_max - $sleep_bw_work_checks_min))
	sleep $sleep_bw_work_checks_min
	sleep $(($RANDOM % $incr))
done
