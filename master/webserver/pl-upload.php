<?php

require("pl-config.php");

$client_host = $_REQUEST["hostname"];
$client_ip = $_SERVER["REMOTE_ADDR"];
$start_addr = $_REQUEST["start_addr"];
$mask = $_REQUEST["mask"];
$output_filename = $_REQUEST["file"];

/* Sanity check */

if ($client_host == "" || $start_addr == "" || $mask == "" || $output_filename == "")
	log_error("Bad PUT from $client_ip");

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
	log_error("Result from wrong host! start_addr = $start_addr, mask = $mask, client_host = $client_host, correct host = ".$row["assigned_to"]);

if ($row["complete"] != false)
	log_error("Result from completed start_addr! start_addr = $start_addr, mask = $mask, host = $client_host");

/* Checks passed -- write the output! */

$putdata = fopen("php://input", "r");
$fp = fopen($output_dir.$output_filename, "w");

while ($data = fread($putdata, 1024))
  fwrite($fp, $data);

fclose($fp);
fclose($putdata);

/* Streams collected -- mark as completed! */

mysql_query("LOCK TABLES $db_table WRITE");
mysql_query("UPDATE $db_table SET complete=True, last_contact=NOW() WHERE start_addr='$start_addr' AND mask='$mask'");
mysql_query("UNLOCK TABLES");

/* Check for barrier condition:
 * If last IP block has been mapped, then we write
 * a marker to the output directory.
 */

$query = "SELECT COUNT(*) AS cnt FROM $db_table WHERE (complete = False OR complete IS NULL)";
$res = mysql_query($query);
if (! $res ) log_error("Bad MySQL result for checking barrier condition!");
$row = mysql_fetch_array($res);

if ($row["cnt"] == "0") {
	$marker_fp = fopen($marker_file, "w");
	fwrite($marker_fp, "Mapping complete");
	fclose($marker_fp);
}

?>
