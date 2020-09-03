<?php
$base_dir="../../system/php";


require_once($base_dir."/page.php");
require_once($base_dir."/authorize.php");

require_once("../../etc/global_variables.php");

$authorized_user_id=authorize();

session_destroy();

/*
$_SESSION["authorize"] = "no";
$_SESSION["authorized_user_id"] = "";
$_SESSION["full_user_name"] = "";
*/

print_refresh_page("http://$HTTP_HOST/$SITE_PATH");
?>

