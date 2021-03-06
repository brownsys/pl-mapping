pl-mapping
==========

Router mapping via PlanetLab

### Setting up master server

 1. Create MySQL user and database
 2. Make sure php5-cli is installed
 3. Install entries in regular & root user's crontabs
 4. Make `pl-uploads` directory on the web server writable by the httpd user
 5. Enable HTTP PUT method using something like:

```
  <Directory /vol/web/html>
   Script PUT /pl-upload.php
   Options FollowSymLinks MultiViews
   AllowOverride All
   Order allow,deny
   allow from all
  </Directory>
``` 

### Rough example for deploying on slaves

```
export MQ_SLICE=brown_map
export MQ_NODES=/home/adf/RouterPeek/pl-mapping/support/nodes.brown_map.txt
ssh-agent
SSH_AUTH_SOCK=/tmp/ssh-LWqws24865/agent.24865; export SSH_AUTH_SOCK;   [for example]
SSH_AGENT_PID=24866; export SSH_AGENT_PID;    [for example]
ssh-add ~/.ssh/pl_key
multicopy client/pl-client.sh @:pl-client.sh
multicopy client/pl-run-client.sh @:pl-run-client.sh
multiquery "/home/brown_map/pl-run-client.sh /home/brown_map/pl-client.sh"
```

Get `multicopy` and `multiquery` from [CoDeploy](http://codeen.cs.princeton.edu/codeploy/)

`nodes.brown_map.txt` and the script to generate it are in the `support` directory

### Running iffinder on quanto

We use quanto to run `iffinder` since it has a direct connection to the internet
and we have root access. The master drops lists of IP addresses on quanto for it
to run iffinder on periodically.

To setup, install the crontab entry which is in the `quanto-iffinder` dir, as
well as the `run-iffinder.sh` script. It is also necessary to create a directory
called `results` and install `iffinder`.
