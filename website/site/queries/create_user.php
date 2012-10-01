<?

 $base_dir="../../system/php";

 require_once($base_dir."/page.php");
 require_once($base_dir."/forms.php");
 require_once($base_dir."/db.php");
 require_once($base_dir."/errors.php");
 require_once($base_dir."/variables.php");

 db_init("user");

 $variables_list=array
 (
	"user_name",
	"login",
	"email"   
 );

 $passwds=array
 (
	"first_passwd",
	"second_passwd"
 );
 
 read_vars($variables_list,"post");
 read_vars($passwds,"post");
 $hash_str=read_var("hash","any");
 
 if ($hash_str!="")
 {
	$query="select user_name,login,email,date_label from hash where hash='$hash_str'";
	$result=db_query($query);
	if (db_num_rows($result)!=1)
	{
		add_error("Bad hash!");
		print_error("Registration error","..");
	}
	db_read_vars($variables_list,$result);
	db_free_result($result);
 }

 

 if ($user_name=="")
	add_error("Empty 'Full name' field!");

 if ($login=="")
	add_error("Empty 'Desired login' field!");

 if ($email=="")
	add_error("Empty 'Email address' field!");


 print_error("Empty or incorrect fields","..");

 


 $query="select user_id from users where ".
	  "email='$email' ".
	  "or login='$login'";

 $result=db_query($query);
 if (db_num_rows($result))
 {
	add_error("User already exists!");
	print_error("Registration error","..");
	db_free_result($result);
 }
 
 if (($hash_str!="") && ($first_passwd=="") && ($second_passwd==""))
 {
	print_page_header("New user registration","..");
		print_form_header("create","../queries/create_user.php");
		/*
		print_hidden_input("first_name",$first_name);
		print_hidden_input("second_name",$second_name);
		print_hidden_input("last_name",$last_name);
		print_hidden_input("academic_group",$academic_group);
		print_hidden_input("email",$email);
		*/
		print_hidden_input("hash",$hash_str);

		print_table_header();
		print_null_input("$user_name","Full name");
		print_null_input($login,"Login");
		print_null_input($email,"Email adress");
		print_password_input("first_passwd","","Password");
		print_password_input("second_passwd","","Confirm password");
		print_table_tail();
		print_submit_input("set","Commit data");
	print_page_tail("..");
	exit(0);
 }


 if (($first_passwd!="") && ($second_passwd!="") && ($hash_str!=""))
 {
	if ($first_passwd!=$second_passwd)
	{
		add_error("Password and its confirmation are different!");
		print_error("Password error","..");
	}

	$query="insert into users set ".
		  "full_user_name='$user_name', ".
		  "login='$login', ".
		  "email='$email', ".
		  "date_of_registration=CURRENT_DATE";

	db_query($query);

	$user_id=db_inserted_id();

	$query="insert into passwords set user_id=$user_id, `password`=password('$first_passwd')";
	db_query($query);

	$query="delete from hash where hash='$hash_str'";
	db_query($query);

	print_refresh_page("../pages/main.php");
	exit(0);
 }

 $query="select login from users where login='$login'";

 $result=db_query($query);
 if (db_num_rows($result))
 {
	add_error("Such login has been already registered!");
	print_error("Registration error","..");
	db_free_result($result);
 }

 $query="select login from hash where login='$login'";
 $result=db_query($query);
 if (db_num_rows($result))
 {
	add_error("Email has been already sent!");
	print_error("Registration error","..");
	db_free_result($result);
 }

 $current_date=date("Y-m-d");

 $hash_str=md5($user_name.$login.$email.$current_date);
 $query="select email from hash where hash='$hash_str'";
 $result=db_query($query);
 if (db_num_rows($result))
 {
	add_error("Attention! Somebody has already tried to register himself. But the registration process was not finished.");
	print_error("Registration error","..");
	db_free_result($result);
 }
 
 $query="insert into hash set ".
	  "user_name='$user_name', ".
	  "login='$login', ".
	  "email='$email', ".
	  "date_label='$current_date', ".
	  "hash='$hash_str'";
	
 db_query($query);

	$text="To activate your account please visit\n";
	$text=$text."\thttps://$HTTPS_HOST/$SITE_PATH/queries/create_user.php?hash=$hash_str";
	$headers=          "From: webmaster@$HTTP_HOST\r\n";
	$headers.=         "Content-Type: text/html; charset=utf8\r\n";
	$headers.=         "X-Mailer: PHP/".phpversion();

 $mail_sent=mail($email,"New account creation",$text,$headers);



 print_page_header("New user registration","..");
 if (!$mail_sent)
 {
	printf("The confirmation email can't be sent!");
 }
 else
 {
	printf("Email with instructions for account activization has been sent.");
 }

// printf("<P><A href=\"http://$HTTP_HOST/$SITE_PATH\">Go to the root page </A></P>");


 print_page_tail("..");
?>

