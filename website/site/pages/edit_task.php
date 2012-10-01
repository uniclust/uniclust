<?
$base_dir="../../system/php";

require_once($base_dir."/page.php");
require_once($base_dir."/forms.php");
require_once($base_dir."/db.php");
require_once($base_dir."/errors.php");
require_once($base_dir."/variables.php");
require_once($base_dir."/authorize.php");

/*
 * Contains $DATA_PATH variable
 */
require_once("../../etc/global_variables.php");

$authorized_user_id=authorize();

db_init("user");


$task_fields=array
(
	"user_id",
	"multiprocessor_id",
	"task_status",
	"date_of_creation",
	"date_of_finishing",
	"num_procs",
	"duration_in_minutes",
	"algorithm",
	"comments"
);

$task_id=(int)read_var("task_id","any");

$result=db_query("select * from tasks where task_id=${task_id}");
if (!db_num_rows($result))
{
	add_error("Task is not registered in database!");
	print_error("Edit task","..");
}
db_read_vars($task_fields,$result);
db_free_result($result);

$mult_id=$multiprocessor_id;

if($authorized_user_id!=$user_id)
{
	add_error("You are not owner of this task!");
	print_error("Edit task","");
}

$query="select multiprocessor_name,num_available_procs,multiprocessor_id from multiprocessors where state='available'";
$result=db_query($query);
$num_multiprocs=db_num_rows($result);

$mult_list=array
(
	"multiprocessor_name",
	"num_available_procs",
	"multiprocessor_id"
);

db_form_arrays($mult_list,$result);
db_free_result($result);

$result=db_query("select distinct algorithm from algorithms_on_multiprocessor");

/*
 Creates array called algorithm
*/
db_form_arrays(array("algorithm"),$result,array("algorithm_list"));
db_free_result($result);

for($i=0;$i<$num_multiprocs;$i++)
{
	$mult_lables[$i]="$multiprocessor_name[$i] ( $num_available_procs[$i] )";
	if ($mult_id==$multiprocessor_id[$i]) $mult_label=$mult_lables[$i];
}

$file_path="${DATA_PATH}/${user_id}/${task_id}/sequences.fasta";

$data_status=file_exists($file_path);

if (($task_status=="submitted") || 
    ($task_status=="stopped") || 
    ($task_status=="ready"))
{
	$task_statuses=array
	(
		"",
		"stopped"
	);
}

if (($task_status=="new") || 
    ($task_status=="refused"))
{
	$task_statuses=array
	(
		"ready",
		"new"
	);
}			

if ($task_status=="finished")
{
	$task_statuses=array
	(
		"finished",
		"ready",
		"new"
	);

}

print_page_header("Edit task","..");
	print_form_header("edit","../queries/edit_task.php");
		print_hidden_input("task_id",$task_id);
		
		if (!$data_status) print_hidden_input("task_status","new");

		print_table_header();
			print_null_input($task_id,"Task ID");
			print_null_input($task_status,"Current task status");
			print_null_input($date_of_creation,"Task creation date");
			print_null_input($date_of_finishing,"Task finishing date");

			if (($task_status=="submitted") || 
			    ($task_status=="stopped") || 
			    ($task_status=="ready"))
			{
				print_hidden_input("multiprocessor_id",$mult_id);
				print_null_input($mult_label,"Multiprocessor with a number of available procs");

				print_hidden_input("num_procs",$num_procs);
				print_null_input($num_procs,"Number of requested procs on a multiprocessor");

				print_hidden_input("algorithm",$algorithm);
				print_null_input($algorithm,"Algorithm");

				print_hidden_input("duration_in_minutes",$duration_in_minutes);
				print_null_input($duration_in_minutes,"Task duration in minutes (Requested CPU time on multiprocessor)");
			}
			else
			{
				print_select_input
				(
					"multiprocessor_id",
					$mult_lables,
					$multiprocessor_id,
					$mult_id,
					"Multiprocessor with a number of available procs"
				);

				print_text_input
				(
					"num_procs",
					$num_procs,
					"Number of requested procs on a multiprocessor"
				);

				/*
				$algorithm_list=array
				(
					"muscle",
					"clustalw"
				);
				*/

				print_select_input
				(
					"algorithm",
					$algorithm_list,
					$algorithm_list,
					$algorithm,
					"Algorithm (change algorithm on ... )"
				);

				print_text_input
				(
					"duration_in_minutes",
					$duration_in_minutes,
					"Task duration in minutes (requested CPU time on multiprocessor)"
				);
			} /* End Else */
			
			if ($data_status)
			{

				print_select_input
				(
					"task_status",
					$task_statuses,
					$task_statuses,
					"",
					"Change task status (leave empty if you don't want to)"
				);

				$str="<a href=\"../pages/data_for_task.php?task_id=${task_id}\"><br>data<br></a>";
				print_null_input($str,"Edit data for this task",false);
			}
			else
			{
				print_null_input("<br>no<br>","Data upload status",false);
			}

			$result=db_query("select seq_type, blast_outp_detail_lvl, lower_thrshld from blast_tasks where task_id=${task_id}");
			if (db_num_rows($result))
			{
				$blast_task_vars=array
				(
					"seq_type",
					"blast_outp_detail_lvl",
					"lower_thrshld"
				);
				db_read_vars($blast_task_vars,$result);
				db_free_result($result);
				
				$values=array("nucleotide","protein");
				print_radio_input("seq_type",$values,$values,$seq_type,"Type of the sequences");
				print_text_input("blast_outp_detail_lvl",$blast_outp_detail_lvl,"BLAST output file detailization level (1..9)");
				print_text_input("simil_thrshld",$lower_thrshld,"Only sequences with similarity not less than this number will be aligned (0..100)");
			}
		print_table_tail();
		
		print_table_header();
			print_textarea_input("comments",$comments,"Comments for this task");
		print_table_tail();

		print_submit_input("set","Update task status");
	print_form_tail();

	if (($task_status!="submitted") && 
	    ($task_status!="stopped") && 
	    ($task_status!="ready"))
	{
		print_file_form_header("data","../queries/add_data.php?task_id=${task_id}");
			print_table_header();
				print_textarea_input("fasta","","Sequences in Fasta format");
			print_table_tail();
	
			print_table_header();
				print_file_input("file","File in Fasta format (size &le; ${MAX_FILE_SIZE} MB)");
			print_table_tail();
			print_submit_input("sbm_button","Upload sequences");
		print_form_tail();
	}

print_page_tail("..");

?>

