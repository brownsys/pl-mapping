<?php

require("pl-config.php");

$mini = $_REQUEST["mini"];

$link = mysql_pconnect($db_host, $db_user, $db_pass);
mysql_select_db($db_name);

$query = "SELECT COUNT(*) AS cnt FROM $db_table WHERE (complete = False OR complete IS NULL)";
$res = mysql_query($query);
if (! $res ) log_error("Bad MySQL result for report!");
$row = mysql_fetch_array($res);
$cnt_incomplete = $row["cnt"];

$query = "SELECT COUNT(*) AS cnt FROM $db_table WHERE complete = True";
$res = mysql_query($query);
if (! $res ) log_error("Bad MySQL result for report!");
$row = mysql_fetch_array($res);
$cnt_complete = $row["cnt"];

$query = "SELECT COUNT(*) AS cnt FROM $db_table WHERE (complete = False OR complete IS NULL) AND assigned_to IS NOT NULL";
$res = mysql_query($query);
if (! $res ) log_error("Bad MySQL result for report!");
$row = mysql_fetch_array($res);
$cnt_inprogress = $row["cnt"];

echo "<table>\n";
echo "<tr><td>Incomplete:</td><td>$cnt_incomplete</td></tr>\n";
echo "<tr><td>Complete:</td><td>$cnt_complete</td></tr>\n";
echo "<tr><td>In Progress:</td><td>$cnt_inprogress</td></tr>\n";
echo "</table><br><br>\n";

if ($mini === "")
	die();

$res = mysql_query("SELECT * FROM $db_table ORDER BY complete DESC, last_contact DESC");
if (! $res ) log_error("Bad MySQL result for report!");

$num = mysql_numrows($res);

echo "<table border='1'>\n";

for ($i = 0; $i < $num; $i++) {
	echo "<tr>";
	echo "<td>";
	echo mysql_result($res, $i, "start_addr");
	echo "</td>";
	echo "<td>";
	echo mysql_result($res, $i, "mask");
	echo "</td>";
    echo "<td>";
    echo mysql_result($res, $i, "assigned_to");
    echo "</td>";
    echo "<td>";
    echo mysql_result($res, $i, "complete");
	echo "</td>";
    echo "<td>";
    echo mysql_result($res, $i, "work_started");
    echo "</td>";
    echo "<td>";
    echo mysql_result($res, $i, "last_contact");
	echo "</td>";
    echo "<td>";
    echo mysql_result($res, $i, "last_addr");
    echo "</td>";
	echo "</tr>\n";
}

echo "</table>";


?>
