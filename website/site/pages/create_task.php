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


$result=db_query("select distinct algorithm from algorithms_on_multiprocessor");

/*
 Creates an array called 'algorithm'
*/
db_form_arrays(array("algorithm"),$result);
db_free_result($result);


/* Old not necessary now.
$algorithm_list=array
(
	"muscle",
	"clustallw"
);
*/

$variables_list=array
(
	"multiprocessor_name",
	"num_available_procs",
	"multiprocessor_id"
);

$query="select multiprocessor_name,num_available_procs,multiprocessor_id from multiprocessors";
$result=db_query($query);
$num_multiprocs=db_num_rows($result);
db_form_arrays($variables_list,$result);
db_free_result($result);

for($i=0;$i<$num_multiprocs;$i++)
{
	$mult_lables[$i]="$multiprocessor_name[$i] ( $num_available_procs[$i] )";	
}


$query="select priority_tokens from users where users.user_id = $authorized_user_id";
$result=db_query($query);
db_form_arrays(array("priority_tokens"),$result);
db_free_result($result);


print_page_header("New task creation","..");
	print_form_header("create","../queries/create_task.php");
		print_table_header();
			print_select_input
			(
				"multiprocessor_id",
				$mult_lables,
				$multiprocessor_id,
				$multiprocessor_id[0],
				"Multiprocessor with a number of available procs"
			);
			print_text_input("num_procs","","Number of requested procs on a multiprocessor");
			print_select_input
			(
				"algorithm",
				$algorithm,
				$algorithm,
				"",
				"Algorithm"
			);
			print_text_input
			(
				"duration_in_minutes",
				"",
				"Task duration in minutes (requested CPU time on multiprocessor)"
			);
			print_text_input("tokens","","Priority tokens for the task (<b>$priority_tokens[0]</b> left)");
		print_table_tail();
		
		print("<br><p style=\"text-align:left\">Fill these fields to group similar sequences using NCBI BLAST (so more than 1 multiple alignment will be made):</p>");
		
		print_table_header();
			print_radio_input
			(
				"seq_type",
				array("nucleotide","protein"),
				array("nucleotide","protein"),
				"nucleotide",
				"Type of the sequences"
			);
			print_text_input("blast_outp_detail_lvl","","BLAST output file detailization level (1..9)");
			print_text_input
			(
				"simil_thrshld",
				"",
				"Only sequences with similarity not less than this number will be aligned (0..100)"
			);
		print_table_tail();
		print_submit_input("set","Create task");
	print_form_tail();
print_page_tail("..");
?>

