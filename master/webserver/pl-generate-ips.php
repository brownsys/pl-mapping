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
		$new_sa = "$quads[0].$quads[1]." . ($quads[2] + ($j * pow(2,(24-$max_mask))))." . $quads[3]";

		$query = "INSERT INTO $db_table VALUES('$new_sa', '$max_mask', NULL, False, NULL, NULL, NULL)";
		mysql_query($query);
	}
	
	// delete the /16
	 mysql_query("DELETE FROM $db_table WHERE start_addr='$sa' AND mask='$mask'");
}

mysql_query("UNLOCK TABLES");

?>
