<?php

require("pl-config.php");

# To help prevent accidents
$processUser = posix_getpwuid(posix_geteuid());
if ($processUser['name'] != "root") {
	echo "script must be run as root!\n";
	die();
}

$link = mysql_pconnect($db_host, $db_user, $db_pass);
mysql_select_db($db_name);

/*

CREATE TABLE pl_mapping (
	start_addr varchar(15) NOT NULL,
	mask varchar(2) NOT NULL,
	assigned_to mediumtext,
	complete boolean,
	work_started datetime DEFAULT NULL,
	last_contact datetime DEFAULT NULL,
	last_addr varchar(15) DEFAULT NULL,
	PRIMARY KEY (start_addr, mask)
);

*/

mysql_query("LOCK TABLES $db_table WRITE");

mysql_query("DELETE FROM $db_table"); # clear it out

# start_addr, mask, assigned_to, complete, work_started, last_contact, last_addr

for ($i = 0; $i < 256; $i++) {
	$query = "INSERT INTO $db_table VALUES('38.$i.0.0', '16', NULL, False, NULL, NULL, NULL)";
	mysql_query($query);
}

mysql_query("INSERT INTO $db_table VALUES('130.117.0.0',   '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('149.6.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.12.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.54.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('173.182.0.0',   '16', NULL, False, NULL, NULL, NULL)"); # unknown if should be smaller
mysql_query("INSERT INTO $db_table VALUES('192.205.0.0',   '16', NULL, False, NULL, NULL, NULL)"); # same
mysql_query("INSERT INTO $db_table VALUES('206.3.64.0',    '18', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.3.32.0',    '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.3.128.0',   '17', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.4.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.5.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.6.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.7.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.112.192.0', '21', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.230.0.0',   '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('212.20.128.0',  '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('64.94.0.0',     '16', NULL, False, NULL, NULL, NULL)"); # unknown if should be smaller
mysql_query("INSERT INTO $db_table VALUES('66.102.96.0',   '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('66.250.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('66.28.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('74.117.104.0',  '21', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('82.138.64.0',   '18', NULL, False, NULL, NULL, NULL)");

## New addresses
## Added 3/22/2013 based on full-internet reverse DNS lookups

mysql_query("INSERT INTO $db_table VALUES('128.241.24.0',  '21', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('130.94.244.0',  '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('149.5.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('149.7.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('149.11.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('149.12.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('149.13.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('149.14.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('149.127.0.0',   '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.6.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.37.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.43.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.44.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.45.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.46.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.48.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.49.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.50.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('154.51.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('157.238.83.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('157.238.90.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('192.77.171.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('192.217.224.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.64.168.0',  '22', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.88.232.0',  '21', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.170.167.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.172.128.0', '20', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.173.150.0', '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.173.159.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.29.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.103.132.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.103.134.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.103.208.0', '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.217.166.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.217.235.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.217.250.0', '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.236.232.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.238.99.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.239.59.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.239.118.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('199.239.216.0', '22', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.0.136.0',   '21', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.2.28.0',    '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.4.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.5.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.6.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.7.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.42.174.0',  '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.42.200.0',  '22', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.57.36.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.57.38.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.57.46.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.143.88.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.157.0.0',   '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.203.0.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('204.233.240.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('205.137.48.0',  '20', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('205.198.0.0',   '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('205.199.0.0',   '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('205.215.0.0',   '18', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('205.238.22.0',  '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.148.0.0',   '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.149.0.0',   '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.0.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.1.0.0',     '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.14.69.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.183.224.0', '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.190.0.0',   '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.222.32.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.222.50.0',  '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.233.94.0',  '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.20.164.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.21.113.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.21.144.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.21.160.0',  '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.31.207.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.31.208.0',  '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.91.101.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.153.64.0',  '18', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.196.73.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.241.0.0',   '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.17.96.0',   '20', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.41.192.0',  '18', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.69.0.0',    '22', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.69.6.0',    '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.69.9.0',    '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.69.36.0',   '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.107.31.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.115.0.0',   '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.139.91.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.146.0.0',   '17', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.157.0.0',   '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.157.165.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.217.128.0', '18', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.227.0.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.227.17.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.227.40.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.227.58.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('213.146.160.0', '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('216.28.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('216.29.0.0',    '16', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('216.44.45.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('216.55.80.0',   '20', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('216.177.96.0',  '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('216.229.128.0', '20', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('217.71.112.0',  '20', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('64.4.192.0',    '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('64.17.48.0',    '20', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('64.202.0.0',    '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('64.254.192.0',  '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('66.71.224.0',   '20', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('80.91.64.0',    '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('80.245.32.0',   '19', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('81.2.128.0',    '18', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('82.129.0.0',    '18', NULL, False, NULL, NULL, NULL)");

##
# None of these blocks are owned by Cogent. However, they contain a few *.cogentco.com entries
# Added 3/22/2013
##

mysql_query("INSERT INTO $db_table VALUES('192.65.185.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('194.59.190.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.32.118.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.32.124.0',  '23', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.32.176.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.32.182.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('198.32.190.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('206.24.241.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('207.188.210.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('208.173.52.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('208.174.226.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.10.13.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('209.234.111.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('212.27.38.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('213.238.34.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('216.191.190.0', '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('66.218.44.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('68.86.89.0',    '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('69.31.63.0',    '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('74.40.26.0',    '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('80.81.192.0',   '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('82.197.128.0',  '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('85.17.36.0',    '24', NULL, False, NULL, NULL, NULL)");
mysql_query("INSERT INTO $db_table VALUES('91.209.117.0',  '24', NULL, False, NULL, NULL, NULL)");

###
# Now split all of the /16, /17, and /18 into /19's
##

$res = mysql_query("SELECT * FROM $db_table WHERE mask < '$max_mask' AND mask >= '16'");

if (! $res ) log_error("Bad MySQL result for split function!");
$num = mysql_numrows($res);

for ($i = 0; $i < $num; $i++) {
	$sa = mysql_result($res, $i, "start_addr");
	$mask = mysql_result($res, $i, "mask");

	$quads = explode(".", $sa);

	for ($j = 0; $j < pow(2, ($max_mask - $mask)); $j++) {
		// compute the /19's and add them
		$new_sa = "$quads[0].$quads[1]." . ($quads[2] + ($j * pow(2,(24-$max_mask)))) . ".$quads[3]";

		$query = "INSERT INTO $db_table VALUES('$new_sa', '$max_mask', NULL, False, NULL, NULL, NULL)";
		mysql_query($query);
	}
	
	// delete the /16
	 mysql_query("DELETE FROM $db_table WHERE start_addr='$sa' AND mask='$mask'");
}

mysql_query("UNLOCK TABLES");

?>
