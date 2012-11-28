<?
$base_dir="../../system/php";

require_once($base_dir."/page.php");
require_once($base_dir."/forms.php");
require_once($base_dir."/db.php");
require_once($base_dir."/errors.php");
require_once($base_dir."/variables.php");
require_once($base_dir."/authorize.php");
require_once($base_dir."/tables.php");

/*
 * Contains $DATA_PATH and $DOWNLOAD_DATA_PATH variables
 */
require_once("../../etc/global_variables.php");

$authorized_user_id=authorize();

db_init("user");

$task_id=(int)read_var("task_id","any");

$result=db_query("select user_id,task_status from tasks where task_id=${task_id}");
if (!db_num_rows($result))
{
    add_error("Task is not registered in the database!");
    print_error("Edit task","..");
}

$db_vars=array("user_id","task_status");
db_read_vars($db_vars,$result);
db_free_result($result);

if ($authorized_user_id!=$user_id)
{
    add_error("You are not owner of this task!");
    print_error("Edit task","");
}


$dir_path="${DATA_PATH}/${user_id}/${task_id}";

$files=scandir($dir_path);


print_page_header("Edit task data","..");

$num_files=count($files);

$headers=array
(
	"Name",
	"Directory/File",
	"Size",
	"Date of modification",
	"Action"
);

print_view_table_header($headers,"List of files:");

if (($task_status=="new") || 
    ($task_status=="finished"))
{
	for ($i=2;$i<$num_files;$i++)
	{
		$file_size=(int)(filesize("$dir_path/$files[$i]")/1024);
		$file_type="file";
		if(is_dir("$dir_path/$files[$i]"))
		{
			$file_type="dir";
		}
		$values=array
		(
			"<A href=\"http://$HTTP_HOST/$DOWNLOAD_DATA_PATH/${user_id}/${task_id}/$files[$i]\">$files[$i]</A>",
			$file_type,
			"$file_size KB",
			date(" j-F-Y G:H ",filemtime("$dir_path/$files[$i]")),
			"<A href=\"../queries/delete_file.php?task_id=${task_id}&file_number=${i}\">delete</A>"
		);
		print_view_table_row($values,False);
	}
}
else
{
	for ($i=2;$i<$num_files;$i++)
	{
		$file_size=(int)(filesize("$dir_path/$files[$i]")/1024);
		$file_type="file";
		if (is_dir("$dir_path/$files[$i]"))
		{
			$file_type="dir";
		}
		$values=array
		(
			"<A href=\"http://$HTTP_HOST/$DOWNLOAD_DATA_PATH/${user_id}/${task_id}/$files[$i]\">$files[$i]</A>",
			$file_type,
			"$file_size KB",
			date(" j-F-Y G:H ",filemtime("$dir_path/$files[$i]")),
			"delete"
		);
		print_view_table_row($values);
	}
}
print_view_table_tail();

printf("<P style=\"text-align:center\">Continue <A href=\"edit_task.php?task_id=${task_id}\">edit task</A> or go to the <A href=\"main.php\">main user page</A></P>");

?>

</BODY>
</HTML>


