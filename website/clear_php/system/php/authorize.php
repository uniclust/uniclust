<?php
require_once("page.php");
require_once("variables.php");
require_once("forms.php");

require_once("../../etc/global_variables.php");

function authorize()
{
	
	/*
	$variables_list=array
	(
		"full_user_name",
		"authorized_user_id"
	);
    */
	session_start();

	$user_id=read_var("authorized_user_id","session");
	$full_user_name=read_var("full_user_name","session");

	$host=$GLOBALS['HTTPS_HOST'];
	$path=$GLOBALS['SITE_PATH'];

	if ($user_id=="")
	{
		print_page_header("Unauthorized user","..");
?>
			<P>You need to authorize yourself. If you have not created an account please visit 
			<a href="../pages/create_user.php">this page</a>. If you forgot the password or if you intend 
			to change it, please visit <a href="../pages/forget_password.php">this page</a>.</P>
<?php
			print_form_header("auth","https://$host/$path/queries/authorize.php");
				print_table_header();
					print_text_input("login","","Login");
					print_password_input("password","","Password");
				print_table_tail();
				print_submit_input("auth","Authorize me");
			print_form_tail();
		print_page_tail("..");
		exit(0);
	}



	return $user_id;
}

?>
