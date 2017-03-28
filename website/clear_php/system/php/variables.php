<?php
/**************************************************************/
function read_var($name,$method,$clear=true)
{
	$post_set=isset($_POST[$name]);
	
	if (($method=="post") && $post_set)
	{
		$var=trim($_POST[$name]);
		if ($clear) $var=str_replace("\r","",$var);
		return $var;
	}
	
	$get_set=isset($_GET[$name]);
	
	if (($method=="get") && $get_set)
	{
		$var=trim($_GET[$name]);
		if ($clear) $var=str_replace("\r","",$var);
		return $var;
	}
	
	$ses_set=isset($_SESSION[$name]);
	
	if (($method=="session") && $ses_set)
	{
		$var=trim($_SESSION[$name]);
		if ($clear) $var=str_replace("\r","",$var);
		return $var;
	}
	
	if ($post_set)
	{
		$var=trim($_POST[$name]);
		if ($clear) $var=str_replace("\r","",$var);
		return $var;
	}
	if ($get_set)
	{
		$var=trim($_GET[$name]);
		if ($clear) $var=str_replace("\r","",$var);
		return $var;
	}
	if ($ses_set)
	{
		$var=trim($_SESSION[$name]);
		if ($clear) $var=str_replace("\r","",$var);
		return $var;
	}
	
	return NULL;
}
/**************************************************************/
function read_vars($names,$method)
{
	$num_vars=count($names);

	for($i=0;$i<$num_vars;$i++)
	{
		$GLOBALS[$names[$i]]=read_var($names[$i],$method);
	}

	return;
}
/**************************************************************/
?>
