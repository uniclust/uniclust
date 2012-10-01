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
$file_number=(int)read_var("file_number","get");

if ($file_number<2)
{
	add_error("File number must be greater than one!");
	print_error("Delete file for task","..");
}

$result=db_query("select task_status,user_id from tasks where task_id=${task_id}");
if (!db_num_rows($result))
{
	add_error("Task is not registered in database!");
	print_error("Delete file for task","..");
}

db_read_vars($task_fields,$result);
db_free_result($result);

if ($user_id!=$authorized_user_id)
{
	add_error("You can't delete files for this task because you are not its owner!");
	print_error("Delete file for task","..");
}

if (($task_status=="submitted") || 
    ($task_status=="stopped") || 
    ($task_status=="ready"))
{
	add_error("Can't delete the file because this task is $task_status!");
	print_error("Delete file for task","..");
}


$task_path="$DATA_PATH/$user_id/$task_id";

$files=scandir($task_path);

if ($file_number>=count($files))
{
	add_error("You have chosen incorrect file number to delete!");
	print_error("Delete file for task","..");	
}

if (system("rm -rf $task_path/$files[$file_number]"))
{
	add_error("Can't delete '$task_path/$files[$file_number]'");
}


print_error("Delete task errors","..");

print_refresh_page("../pages/data_for_task.php?task_id=${task_id}");

?>

