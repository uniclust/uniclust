<?php

include_once("../../etc/global_variables.php");


/***************************************************************************/
function print_page_header($page_name,$www_prefix)
{
 
  if($session_started!="true")
  {
  	session_start();
	$session_started="true";
  }
  
?>
<HTML>
<HEAD>
  <meta http-equiv="Content-Type" content="text/html; charset=utf8">
<?php
	printf("<link rel=\"stylesheet\" href=\"%s/css/style.css\">",$www_prefix);
	printf("<title> %s </title>",$page_name);
?>
</HEAD>
<BODY>

 <P>
  <TABLE width="100%">
  <TR>
   <TD width="10%">
<?php
	printf
	(
		"<A href=\"http://%s/%s\"><IMG src=\"%s/images/logotype.jpg\" height=\"120\" width=\"240\" alt=\"\" border=\"0\"></A>",
		$GLOBALS["HTTP_HOST"],
		$GLOBALS["SITE_PATH"],
		$www_prefix
	);
	
?>
   </TD>
   <TD width="90%">
    <DIV class="page_name">
<?php
	printf("%s",$page_name);
?>
    </DIV>
   </TD>
  </TR>
  </TABLE>
 </P>
 <P style="text-align:left">
   On any question please send an email to <A href="mailto:salnikov@cs.msu.su">
   <I>Alexey Salnikov</I></A>
 </P>
 <br>
<?php
}

/****************************************************************************/
function print_page_tail($www_prefix)
{
	printf("<center><A href=\"%s/pages/main.php\">Go to the user page</A></center>",$www_prefix);
?>
 
 </BODY>
 </HTML>
<?php
}

/****************************************************************************/
function print_refresh_page($url)
{

/*
  if($session_started!="true")
  {
  	session_start();
	$session_started="true";
  }
*/

?>
<HTML>
<HEAD>
<?php
	printf(" <META http-equiv=\"refresh\" content=\" 0; URL=%s\">",$url);
?>
</HEAD>
</HTML>

<?php
}
/***************************************************************************/
?>
