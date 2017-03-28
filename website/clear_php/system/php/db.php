<?php
require_once("../../etc/global_variables.php");
require_once("page.php");


/*
echo ($DB_NAME);
echo(realpath("../../../etc/global_variables.php"));
*/

$db_id;

/*
 *
 * DB initialization
 *
 */
function db_init($access_type)
{
	global $DB_NAME;
	global $DB_USER;
	global $DB_USER_PASSWORD;
	global $DB_GUEST_USER;
	global $DB_GUEST_PASSWORD;
	global $DB_HOST;
	global $db_id;
	

	if($access_type == "user")
	{
		$db_user=$DB_USER;
		$db_passw=$DB_USER_PASSWORD;
	}

	if($access_type == "guest")
	{
		$db_user=$DB_GUEST_USER;
		$db_passw=$DB_GUEST_PASSWORD;
	}
	
	$db_id=mysql_connect($DB_HOST,$db_user,$db_passw);
	if(!$db_id)
	{
		print_page_header("Data base connection error","..");
		printf("<P>\n Can not connect to the database:<BR>\n %s \n</P>\n",mysql_error());
		print_page_tail("..");
		exit();
	}

	if(!mysql_select_db($DB_NAME,$db_id))
	{
		print_page_header("Data base selection error","..");
		printf("<P> Can not select database: '%s' <BR>\n %s \n</P>\n",$DB_NAME,mysql_error());
		print_page_tail("..");
		mysql_close($db_id);
		exit();
	}

	mysql_query ("set character_set_client = 'koi8r'",$db_id);
	mysql_query ("set character_set_results = 'koi8r'",$db_id);
	mysql_query ("set character_set_connection ='koi8r'",$db_id);
	mysql_query ("set collation_connection = 'koi8r_general_ci'",$db_id);

	return;

}

/*
 * Query to database
 */
function db_query($query)
{
	global $db_id;
	
	$result=mysql_query($query,$db_id);
	if(!$result)
	{
		print_page_header("Data base query error","..");
		printf("<P>\n Query failed:<BR>\n <B><I>'%s'</I></B> \n</P>\n",$query);
		printf("<P>\n Error:<BR>\n <B><I> '%s' </I></B> \n</P>\n",mysql_error());
		print_page_tail("..");
		mysql_close($db_id);
		exit();
	}

	return $result;
}

/*
 * Number of rows in result
 */
function db_num_rows($result)
{
	return mysql_num_rows($result);
}

/*
 * fetch association
 */
function db_fetch_assoc($result)
{
	return mysql_fetch_assoc($result);
}

/*
 *
 * free result
 *
 */
function db_free_result($result="")
{
	if($result)
		 mysql_free_result($result);
}

/*
 *
 * read results
 *
 */
function db_read_vars($variables,$result)
{
	$num_vars=count($variables);
	$data=db_fetch_assoc($result);
	for($i=0;$i<$num_vars;$i++)
	{
		$GLOBALS[$variables[$i]]=$data[$variables[$i]];
	}

	return;
}

function db_read_var($var_name,$result)
{
	$data=db_fetch_assoc($result);
	return $data[$var_name];
}


/*
 * Creates data array in memory 
 */
function db_form_arrays($arrays_names,$result,$result_arrays_names=array())
{
	$data_size=db_num_rows($result);
	// no data - empty array!
	if (!$data_size) return;
	
	$num_vars=count($arrays_names);
	
	$arr=array(array());
	
	for($i=0;$i<$data_size;$i++)
	{
		$data=db_fetch_assoc($result);
		for($j=0;$j<$num_vars;$j++)
		{
			$arr[$j][$i]=$data[$arrays_names[$j]];
		}
	}
	
	if (count($result_arrays_names)!=0)
	{
		for($i=0;$i<$num_vars;$i++)
		{
			$GLOBALS[$result_arrays_names[$i]]=$arr[$i];
		}
	}
	else
	{
		for($i=0;$i<$num_vars;$i++)
		{
			$GLOBALS[$arrays_names[$i]]=$arr[$i];
		}
	}
	unset($arr);
	
	return;
}

/*
 *
 * Last inserted id in database
 *
 */
function db_inserted_id()
{
	return mysql_insert_id();
}

?>
