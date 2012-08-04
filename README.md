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
