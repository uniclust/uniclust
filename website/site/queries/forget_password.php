<?php
$base_dir="../../system/php";

require_once($base_dir."/page.php");
require_once($base_dir."/forms.php");
require_once($base_dir."/db.php");
require_once($base_dir."/errors.php");
require_once($base_dir."/variables.php");

db_init("user");


$db_variables_list=array
(
	"user_name",
	"login",
	"user_id"
);
$passwds=array
(
	"first_passwd",
	"second_passwd"
);

read_vars($passwds,"post");
$hash_str=read_var("hash","any");

$login=read_var("login","post");

if($hash_str!="")
{
	$query="select hash.user_name,hash.login,users.user_id from hash,users where hash='$hash_str' and hash.login=users.login";
	$result=db_query($query);
	if(db_num_rows($result)!=1)
	{
		add_error("Attention! Bad hash!");
		print_error("Registration errors","..");
	}
	
	db_read_vars($db_variables_list,$result);
}

if(($hash_str!="")&&($first_passwd=="")&&($second_passwd==""))
{
	print_page_header("Password restore","..");
		print_form_header("create","../queries/forget_password.php");
		
		/*
		print_hidden_input("first_name",$first_name);
		print_hidden_input("second_name",$second_name);
		print_hidden_input("last_name",$last_name);
		print_hidden_input("academic_group",$academic_group);
		print_hidden_input("email",$email);
		*/
		print_hidden_input("hash",$hash_str);
		

		print_table_header();
			print_null_input($user_name,"Full user name");
			print_null_input($login,"Login");
			print_password_input("first_passwd","","Password");
			print_password_input("second_passwd","","Confirm password");
		print_table_tail();
		print_submit_input("set","Set password");
	print_page_tail("..");
	exit(0);
}

if (($first_passwd!="") && ($second_passwd!="") && ($hash_str!=""))
{
	if ($first_passwd!=$second_passwd)
	{
		add_error("'Password' and 'Password confirmation' fields differ!");
		print_error("Password restore","..");
	}
	
	$query="update passwords set `password`=password('$first_passwd') where user_id=$user_id";
	db_query($query);
	
	$query="delete from hash where hash='$hash_str'";
	db_query($query);
	print_refresh_page("../pages/main.php");
	exit(0);
}

if ($login=="")
{
	add_error("Empty 'Login' field!");
	print_error("Errors","..");
}

$query="select full_user_name,user_id from users where login='$login'";
$result=db_query($query);
if (db_num_rows($result)==1)
{
   
	$variables_list=array
	(
		"full_user_name",
		"user_id"
	);
	db_read_vars($variables_list,$result);
	db_free_result($result);
	
	$query="select date_label from hash where login='$login'";
	$result=db_query($query);
	if (db_num_rows($result))
	{
		$req_data=db_read_var("date_label",$result);
		add_error("You have already had a request on $req_data. Please wait until 24 hours expire if you want another request.");
		print_error("Existing request","..");
		db_free_result($result);
	}


	$query="select email from users where user_id=$user_id";
	$result=db_query($query);
	$num_emails=db_num_rows($result);
	
	for ($i=0;$i<$num_emails;$i++)
	{
		$data=db_fetch_assoc($result);
		$emails[$i]=$data['email'];
		$query="delete from hash where email='${emails[$i]}'";
		db_query($query);
	}
	db_free_result($result);
	
	$current_date=date("Y-m-d");

	$hash_str=md5($full_user_name.$login.$emails[0].$current_date);

	$query="insert into hash set ".
		  "user_name='$full_user_name', ".
		  "login='$login', ".
		  "email='${emails[0]}', ".
		  "date_label='$current_date', ".
		  "hash='$hash_str'";

	/*
	echo($query);
	exit(0);
	*/

	db_query($query);

	$text="To restore password please visit:\n";
	$text.="\thttps://$HTTPS_HOST/$SITE_PATH/queries/forget_password.php?hash=$hash_str";
	$headers =         "From: webmaster@$HTTP_HOST\r\n";
	$headers.=         "Content-Type: text/html; charset=utf8\r\n";
	$headers.=         "X-Mailer: PHP/".phpversion();
	
	for ($i=0;$i<$num_emails;$i++)
	{
		mail($emails[$i],"Restore password",$text,$headers);
	}
}

print_page_header("Password restore","..");
?>
 <p>
   Read email in your mailbox.
 </p>
<?php
print_page_tail("..");

?>

