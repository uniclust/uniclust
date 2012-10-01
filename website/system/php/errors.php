<?
require_once("page.php");

$error_string="";

/******************************************************************/
function add_error($err,$filter=True)
{
    global $error_string;
    if($filter) $err=htmlspecialchars($err);
	$error_string.="  <P>$err</P>\n\n";
	return;
}
/*****************************************************************/
function print_error($name,$base)
{
	global $error_string;

	if($error_string!="")
	{
		print_page_header($name,$base);
		echo($error_string);
		print_page_tail($base);
		exit();
	}

	return;
}
/*****************************************************************/
	
?>
