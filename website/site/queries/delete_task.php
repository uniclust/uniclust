<?
$base_dir="../../system/php";

require_once($base_dir."/page.php");
require_once($base_dir."/forms.php");
require_once($base_dir."/db.php");
require_once($base_dir."/errors.php");
require_once($base_dir."/variables.php");
require_once($base_dir."/authorize.php");

require_once("../../etc/global_variables.php");


$authorized_user_id=authorize();

db_init("user");


$task_fields=array
(
	"user_id",
	"task_status"
);


$task_id=(int)read_var("task_id","get");

$result=db_query("select task_status,user_id from tasks where task_id=${task_id}");
if (!db_num_rows($result))
{
	add_error("Task is not registered in database");
	print_error("Delete task","..");
}

db_read_vars($task_fields,$result);
db_free_result($result);

if ($user_id!=$authorized_user_id)
{
	add_error("You can't delete this task because you are not its owner!");
	print_error("Delete task","..");
}

if (($task_status=="submitted") || 
    ($task_status=="stopped") || 
    ($task_status=="ready"))
{
	add_error("Can't delete $task_status task!");
	print_error("Delete task","..");
}


$path="$DATA_PATH/$user_id/$task_id";
if (system("rm -rf $path"))
{
	add_error("Can't delete '$path'!");
}

$query="delete from tasks where task_id=$task_id";
db_query($query);

$query="delete from blast_tasks where task_id=$task_id";
db_query($query);

print_error("Delete task errors","..");

print_refresh_page("../pages/main.php");

?>

