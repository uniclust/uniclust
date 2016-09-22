<?php

 $base_dir="../../system/php";

 require_once($base_dir."/page.php");
 require_once($base_dir."/forms.php");

 require_once("../../etc/global_variables.php");
 
 print_page_header("Password recovery","..");
?>

 <P>
  If you forgot your password you can recover it by means of login and email.<br>
  Type them on the registration page and you will receive an email with a special key.   
 </P>
<?php

 printf("<P><A href=\"http://$HTTP_HOST/$SITE_PATH\">Go to the root page</A></P>");


 print_form_header("auth","../queries/forget_password.php");
	print_table_header();
		print_text_input("login","","Login");
	print_table_tail();
	print_submit_input("auth","Recover");
 print_form_tail();
 print_page_tail("..");
?>

