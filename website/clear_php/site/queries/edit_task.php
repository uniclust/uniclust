<?php
$base_dir="../../system/php";

require_once($base_dir."/page.php");
require_once($base_dir."/forms.php");
require_once($base_dir."/db.php");
require_once($base_dir."/errors.php");
require_once($base_dir."/variables.php");
require_once($base_dir."/authorize.php");


$authorized_user_id=authorize();

db_init("user");


$task_fields=array
(
	"task_id",
	"multiprocessor_id",
	"task_status",
	"num_procs",
	"duration_in_minutes",
	"algorithm",
	"comments",
	
	"seq_type",
	"blast_outp_detail_lvl",
	"simil_thrshld"
);

read_vars($task_fields,"post");

$task_id=(int)$task_id;
$multiprocessor_id=(int)$multiprocessor_id;
$num_procs=(int)$num_procs;
$duration_in_minutes=(int)$duration_in_minutes;

$result=db_query("select task_status,user_id from tasks where task_id=${task_id}");
if (!db_num_rows($result))
{
	add_error("Task is not registered in database!");
	print_error("Edit task","..");
}

$data=db_fetch_assoc($result);
$old_task_status=$data["task_status"];
$user_id=$data["user_id"];
db_free_result($result);

if ($authorized_user_id!=$user_id)
{
	add_error("You are not owner of this task!");
	print_error("Edit task","..");
}

if ($multiprocessor_id<=0)
{
	add_error("Multiprocessor is not chosen!");
	print_error("Edit task","..");
}


$result=db_query("select num_available_procs,multiprocessor_name from multiprocessors where multiprocessor_id=${multiprocessor_id}");
$data=db_fetch_assoc($result);
$num_avail_procs=$data["num_available_procs"];
$multiprocessor_name=$data["multiprocessor_name"];
db_free_result($result);

if ($num_procs<=0) add_error("Bad number of processors!");
else
{
	if ($num_procs > $num_avail_procs) add_error("Number of requested processors is greater than number of the available ones!");
}

if ($task_status=="")
{
	add_error("Empty task status!");
}

if ($duration_in_minutes<=0)
{
	add_error("Bad time duration!");
}

if ($algorithm=="")
{
	add_error("Bad algorithm name!");
}

/*
if($algorithm=="clustalw")
{
	add_error("Sorry, clustalw not supported yet.");
}
*/

print_error("Update task errors","..");

$result=db_query("select algorithm from algorithms_on_multiprocessor where algorithm=\"$algorithm\" and multiprocessor_id=$multiprocessor_id");
if(!db_num_rows($result))
{
    add_error("Algorithm '$algorithm' is not registered on multiprocessor '$multiprocessor_name'!");
    print_error("Update task errors","..");
}
db_free_result($result);

$query="update tasks set ".
	   "multiprocessor_id=$multiprocessor_id, ".
	   "duration_in_minutes=$duration_in_minutes, ".
	   "num_procs=$num_procs, ".
	   "task_status=\"${task_status}\", ".
		"comments=\"$comments\",".
	   "algorithm=\"$algorithm\" ".
	   "where task_id=$task_id";
db_query($query);

if (($blast_outp_detail_lvl!="") && ($simil_thrshld!=""))
{
	$query="update blast_tasks set ".
		  "task_id=$task_id, ".
		  "seq_type=\"$seq_type\", ".
		  "blast_outp_detail_lvl=$blast_outp_detail_lvl, ".
		  "lower_thrshld=$simil_thrshld";
	db_query($query);
}
else db_query("delete from blast_tasks where task_id=${task_id}");

print_refresh_page("../pages/edit_task.php?task_id=${task_id}");

?>
