<?

 $base_dir="../../system/php";

 require_once($base_dir."/page.php");
 require_once($base_dir."/forms.php");
 require_once($base_dir."/variables.php");
 require_once($base_dir."/authorize.php");
 require_once($base_dir."/db.php");
 require_once($base_dir."/errors.php");
 require_once($base_dir."/tables.php");

 $authorized_user_id=authorize();

 db_init("user");
 
 $db_variables_list=array
 (
	"login",
	"date_of_registration",
	"email",
	"full_user_name"
 );
 $multiprocessors_list=array
 (
	"multiprocessor_id",
	"que_multiprocessor_name",
	"home_page"
  );
 $query="select priority_tokens from users where users.user_id = $authorized_user_id";
 $result=db_query($query);
 db_form_arrays(array("priority_tokens"),$result);
 db_free_result($result);

 $query="select * from users where user_id=${authorized_user_id}";

 $result=db_query($query);
 if (!db_num_rows($result))
	 add_error("The user is not registered in the databse!");

 db_read_vars($db_variables_list,$result);
 print_error("Errors","..");

 db_free_result($result);
 $query="select multiprocessor_id, multiprocessor_name as que_multiprocessor_name, site_url as home_page from multiprocessors";
 $result2=db_query($query);
 $num_mult=db_num_rows($result2);
 db_form_arrays($multiprocessors_list,$result2);
 db_free_result($result2);

 /*
  * Read user tasks.
  */ 
 /*$query="select tasks.task_id, multiprocessors.multiprocessor_name, multiprocessors.site_url, algorithm, duration_in_minutes, num_procs, task_status, date_of_creation, date_of_finishing";*/
 $query="select tasks.task_id, multiprocessors.multiprocessor_name, algorithm, duration_in_minutes, num_procs, task_status, date_of_creation, date_of_finishing";
 $query.=" from tasks,multiprocessors where user_id=${authorized_user_id} and multiprocessors.multiprocessor_id=tasks.multiprocessor_id";

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
//	 "site_url"
 );

 db_form_arrays($db_vars,$result);
 db_free_result($result);

 print_page_header("Personal page of the user","..");

 print_table_header();
 	print_null_input($full_user_name,"Full name");
	print_null_input($login,"Login");
	print_null_input($date_of_registration,"Date of registration");
	print_null_input($email,"Email address");
	print_null_input($priority_tokens[0],"Number of Tokens");
 print_table_tail("..");

/* XXX Uncomment it when user_info_edit.php will be written
 print_action_table_header();
 	print_action_table_command("edit","user_info_edit.php","..","Edit user info");
 print_action_table_tail();
*/
 
 
 if ($num_tasks)
 {
	$header_arr=array
	(
		"Task ID",
		"Multiprocessor",
		"Requested time, minutes",
		"Requested processors",
		"Using BLAST",
		"Status",
		"Algorithm",
		"Creation date",
		"Finishing date",
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
	
	for ($i=0;$i<$num_tasks;$i++)
	{
		for ($j=0; ($j<$num_tasks_with_blast) && ($blast_task_id[$j]!=$task_id[$i]); $j++) ;
		if ($j<$num_tasks_with_blast) $using_blast="yes";
		else $using_blast="no";
		$manage_str="<a href=\"../pages/edit_task.php?task_id=${task_id[$i]}\">edit</a>,&nbsp;<a href=\"../queries/delete_task.php?task_id=${task_id[$i]}\">delete</a>";
		$row=array
		(
			"$task_id[$i]",
			//"<A href=\"$site_url[$i]\">$multiprocessor_name[$i]</A>",
			// swap these two lines
			$multiprocessor_name[$i],
			"$duration_in_minutes[$i]",
			"$num_procs[$i]",
			$using_blast,
			$task_status[$i],
			$algorithm[$i],
			"$date_of_creation[$i]",
			"$date_of_finishing[$i]",
			$manage_str
		);
        print_view_table_row($row,False /* Not apply HTML filter */);
	}
	
	print_view_table_tail();
 }
 else // no user tasks
 {
	printf("Tasks:<br><br>");
	printf("<center><TABLE border=\"\">");
	printf("<TR>");
	printf("<TH class=\"general\">");
	printf("<font size=\"+2\">&nbsp;No tasks&nbsp;</font>");
	printf("</TH>");
	printf("</TR>");
	printf("</TABLE></center>");
 }
 
 print_action_table_header();
   print_action_table_command("create","create_task.php","..","Create new task");
 print_action_table_tail();


 $header_arr=array
 (
	"name",
	"home page"
 );
 print_view_table_header($header_arr,"<br>Queue on multiprocessor:");
 for($i=0;$i<$num_mult;$i++)
 {
 	$row=array
	(
		"<a href=\"../pages/mult_queue.php?mult_id=${multiprocessor_id[$i]}\">$que_multiprocessor_name[$i]</a>",
		"<a href=\"$home_page[$i]\">--></a>"
	);
    print_view_table_row($row,False /* Not apply HTML filter */);
 }
 print_view_table_tail();

 printf("<P style=\"text-align:center\"><A href=\"http://$HTTP_HOST/$SITE_PATH\">Go to the root page</A> or <A href=\"logout.php\">logout</A></P>");
?>

</BODY>
</HTML>

