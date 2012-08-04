<?php

$db_host = "localhost";
$db_user = "pl_mapping";
$db_pass = "pl_mapping";
$db_name = "pl_mapping";
$db_table = "pl_mapping";

# for when no more work is available
$sleep_when_told=43200; # 12 hours
# maximum size of CIDR blocks to scan
$max_mask = 19;  # must betwen < 24 & >= 16

$output_dir = "pl-uploads/";
$err_file = $output_dir."pl-errors.txt";
$marker_file = $output_dir."__MAPPING_COMPLETE__";

/* Error logging function */
function log_error($msg) {
    global $err_file;

    $fp = fopen($err_file, "a");
    fwrite($fp, $msg."\n");
    fclose($fp);
    die();
}

?>
