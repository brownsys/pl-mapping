<?php

require("pl-config.php");

$client_host = $_REQUEST["hostname"];
$client_ip = $_SERVER["REMOTE_ADDR"];

/* Sanity check */

if ($client_host == "")
	log_error("Bad pl-get-work from $client_ip");

$ip = gethostbyname($client_host);

if ($ip != $client_ip)
	log_error("DNS lookup failed for host: $client_host Expected: $client_ip Got: $ip");

/* Checks passed -- give it some work! */

$link = mysql_pconnect($db_host, $db_user, $db_pass);
mysql_select_db($db_name);

mysql_query("LOCK TABLES $db_table WRITE");

$query = "SELECT * FROM $db_table WHERE (assigned_to IS NULL) OR (complete = False AND last_contact < DATE_SUB(NOW(), INTERVAL 3 HOUR)) ORDER BY RAND() LIMIT 1"; # this is a slow way to get a random row, but who cares?

$res = mysql_query($query);

if (! $res || mysql_num_rows($res) < 1) {
	echo "MAPPING_COMMAND:sleep:$sleep_when_told";
	mysql_query("UNLOCK TABLES");
	die();
}

$row = mysql_fetch_array($res);
$start_addr = $row["start_addr"];
$mask = $row["mask"];

echo "MAPPING_COMMAND:$start_addr:$mask";

mysql_query("UPDATE $db_table SET assigned_to='$client_host', work_started=NOW(), last_contact=NOW() WHERE start_addr='$start_addr' AND mask='$mask'");
mysql_query("UNLOCK TABLES");

?>
