<?php

require("pl-config.php");

$client_host = $_REQUEST["hostname"];
$client_ip = $_SERVER["REMOTE_ADDR"];
$start_addr = $_REQUEST["start_addr"];
$mask = $_REQUEST["mask"];
$last_addr = $_REQUEST["last_addr"];

/* Sanity check */

if ($client_host == "" || $start_addr == "" || $mask == "" || $last_addr == "")
	log_error("Bad worker ping from $client_ip");

$ip = gethostbyname($client_host);

if ($ip != $client_ip)
	log_error("DNS lookup failed for host: $client_host Expected: $client_ip Got: $ip");

/* Consistency check */

$link = mysql_pconnect($db_host, $db_user, $db_pass);
mysql_select_db($db_name);

$query = "SELECT * FROM $db_table WHERE start_addr='$start_addr' AND mask='$mask'";
$res = mysql_query($query);

if (! $res ) log_error("Bad MySQL result with start_addr = $start_addr, mask = $mask");
$row = mysql_fetch_array($res);

if ($row["assigned_to"] != $client_host)
	log_error("Working ping from wrong host! start_addr = $start_addr, mask = $mask, client_host = $client_host, correct host = ".$row["assigned_to"]);

if ($row["complete"] != false)
	log_error("Worker ping from completed start_addr! start_addr = $start_addr, mask = $mask, host = $client_host");

/* Checks passed -- record most recent contact! */

mysql_query("LOCK TABLES $db_table WRITE");
mysql_query("UPDATE $db_table SET last_contact=NOW(), last_addr='$last_addr' WHERE start_addr='$start_addr' AND mask='$mask'");
mysql_query("UNLOCK TABLES");

?>
