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
  * Contains $DATA_PATH variable
  */
 require_once("../../etc/global_variables.php");

 $authorized_user_id=authorize();
 db_init("user");

 $mult_id=(int)read_var("mult_id","any");
 
 /*$query="select tasks.task_id, multiprocessors.multiprocessor_name, multiprocessors.site_url, algorithm, duration_in_minutes, num_procs, task_status, date_of_creation, date_of_finishing, running_time, tasks.user_id, login ";*/
 $query="select tasks.task_id, multiprocessors.multiprocessor_name, algorithm, duration_in_minutes, num_procs, task_status, date_of_creation, date_of_finishing, running_time, tasks.user_id, login ";
 $query.=" from tasks,multiprocessors,users where users.user_id=tasks.user_id and multiprocessors.multiprocessor_id=${mult_id} and multiprocessors.multiprocessor_id=tasks.multiprocessor_id order by task_id desc";

 $result=db_query($query);
 $num_tasks=db_num_rows($result);

 $db_vars=array
 (
	 "task_id",
	 "multiprocessor_name",
	 "duration_in_minutes",
	 "num_procs",
	 "task_status",
	 "algorithm",
	 "date_of_creation",
	 "date_of_finishing",
	 "running_time",
//	 "site_url",
	 "user_id",
	 "login"
 );

 db_form_arrays($db_vars,$result);
 db_free_result($result);

 print_page_header("Task queue on multiprocessor \"$multiprocessor_name[0]\"","..");
 print_page_tail("..");

 $header_arr=array
 (
	"Task ID",
//	"Multiprocessor",
	"Requested time, minutes",
	"Requested processors",
	"Using BLAST",
	"Status",
	"Algorithm",
	"Creation date",
	"Running time",
	"Finishing date",
	"User",
	"Manage"
 );

 print_view_table_header($header_arr,"Tasks:");
 
 $result=db_query("select task_id as blast_task_id from blast_tasks");
 $num_tasks_with_blast=db_num_rows($result);
 if ($num_tasks_with_blast>0)
 {
	db_form_arrays(array("blast_task_id"),$result);
	db_free_result($result);
 }
	
 for($i=0;$i<$num_tasks;$i++)
 {
	for ($j=0; ($j<$num_tasks_with_blast) && ($blast_task_id[$j]!=$task_id[$i]); $j++) ;
	if ($j<$num_tasks_with_blast) $using_blast="yes";
	else $using_blast="no";
	if ($user_id[$i] == $authorized_user_id)
	{
		$manage_str="<a href=\"../pages/edit_task.php?task_id=${task_id[$i]}\">edit</a>,&nbsp;<a href=\"../queries/delete_task.php?task_id=${task_id[$i]}\">delete</a>";
		$row=array
		(
			"$task_id[$i]",
//			"<A href=\"$site_url[$i]\">$multiprocessor_name[$i]</A>",
			"$duration_in_minutes[$i]",
			"$num_procs[$i]",
			$using_blast,
			$task_status[$i],
			$algorithm[$i],
			"$date_of_creation[$i]",
			"$running_time[$i]",
			"$date_of_finishing[$i]",
			$login[$i],
			$manage_str
		);
	}
	else
	{
		$row=array
		(
			"$task_id[$i]",
//			"<A href=\"$site_url[$i]\">$multiprocessor_name[$i]</A>",
			"$duration_in_minutes[$i]",
			"$num_procs[$i]",
			$using_blast,
			$task_status[$i],
			$algorithm[$i],
			"$date_of_creation[$i]",
			"$running_time[$i]",
			"$date_of_finishing[$i]",
			$login[$i],
			""
		);
	}
	print_view_table_row($row);
 }
 print_view_table_tail();
 print_action_table_header();
   print_action_table_command("create","create_task.php","..","Create new task");
 print_action_table_tail();


 printf("<P align=\"center\"><A href=\"http://$HTTP_HOST/$SITE_PATH\">Go to the root page</A> or <A href=\"logout.php\">logout</A></P>");

?>

