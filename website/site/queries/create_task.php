<?
$base_dir="../../system/php";

require_once($base_dir."/page.php");
require_once($base_dir."/forms.php");
require_once($base_dir."/db.php");
require_once($base_dir."/errors.php");
require_once($base_dir."/variables.php");
require_once($base_dir."/authorize.php");

$authorized_user_id=authorize();

db_init("user");

//echo("test2");
$task_fields=array
(
	"multiprocessor_id",
	"num_procs",
	"duration_in_minutes",
	"algorithm",
	"tokens",
	
	"seq_type",
	"blast_outp_detail_lvl",
	"simil_thrshld"
);

read_vars($task_fields,"post");
$tokens = (int)$tokens;
$multiprocessor_id=(int)$multiprocessor_id;
$num_procs=(int)$num_procs;
$duration_in_minutes=(int)$duration_in_minutes;

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

if ($duration_in_minutes<=0) add_error("Bad time duration!");

if ($algorithm=="") add_error("The algorithm was not chosen!");

print_error("Create task errors","..");

$result=db_query("select algorithm from algorithms_on_multiprocessor where algorithm=\"$algorithm\" and multiprocessor_id=$multiprocessor_id");
if (!db_num_rows($result))
{
	add_error("Algorithm '$algorithm' is not registered on multiprocessor \"$multiprocessor_name\"!");
	print_error("Create task errors","..");
}
db_free_result($result);


$query="insert into tasks set ".
	   "user_id=$authorized_user_id, ".
	   "multiprocessor_id=$multiprocessor_id, ".
	   "duration_in_minutes=$duration_in_minutes, ".
	   "num_procs=$num_procs, ".
	   "task_status=\"new\", ".
	   "algorithm=\"$algorithm\", ".
	   "date_of_creation=CURRENT_DATE, ".
	   "priority_max=$tokens, ".
	   "priority_run=$tokens ";
db_query($query);

$task_id=db_inserted_id();

if (($blast_outp_detail_lvl!="") && ($simil_thrshld!=""))
{
	$query="insert into blast_tasks set ".
		  "task_id=$task_id, ".
		  "seq_type=\"$seq_type\", ".
		  "blast_outp_detail_lvl=$blast_outp_detail_lvl, ".
		  "lower_thrshld=$simil_thrshld";
	db_query($query);
}

$query="update users set ".
       "users.priority_tokens=users.priority_tokens-$tokens ".
	   "where users.user_id=$authorized_user_id ";

db_query($query);


print_refresh_page("../pages/edit_task.php?task_id=${task_id}");

?>
