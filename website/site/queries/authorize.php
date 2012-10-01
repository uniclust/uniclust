<?
$base_dir="../../system/php";


require_once($base_dir."/db.php");
require_once($base_dir."/page.php");
require_once($base_dir."/variables.php");
require_once($base_dir."/errors.php");

session_start();

$variables_list=array
(
	"login",
	"password"
);

$db_var_list=array
(
	"user_id",
	"full_user_name"
);

read_vars($variables_list,"post");

if($login=="") add_error("Empty 'Login' field!");

if($password=="") add_error("Empty 'Password' field!");

print_error("Authorize error","..");

/*
echo( $email);
echo( $password);
*/

db_init("user");

$query="select users.user_id,users.full_user_name from users,passwords where users.login = '$login' and users.user_id = passwords.user_id and passwords.password = password('$password') ";
$result=db_query($query);
if(!db_num_rows($result)) add_error("Bad user name or password!");

db_read_vars($db_var_list,$result);
db_free_result($result);

/*
 * Set up errors first (use 'add_error' function)!
 */
print_error("Authorize error","..");

$_SESSION = array();

$_SESSION["authorize"] = "yes";
$_SESSION["authorized_user_id"] = $user_id;
$_SESSION["full_user_name"] = $full_user_name;

session_write_close();

db_query("update users set last_login=CURRENT_DATE where user_id=$user_id");

print_refresh_page("../pages/main.php");
  

?>

