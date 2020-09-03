<?php
$base="../../system/php";


require_once($base."/page.php");
require_once($base."/forms.php");
require_once($base."/errors.php");
require_once($base."/variables.php");
require_once($base."/authorize.php");
require_once($base."/db.php");

/*
 * Contains $DATA_PATH variable
 */
require_once("../../etc/global_variables.php");

$authorized_user_id=authorize();
db_init("user");



$fasta=read_var("fasta","any");
$task_id=(int)read_var("task_id","any");

$tmp_file_name =  $_FILES["file"]["tmp_name"];
$tmp_file_size =  $_FILES["file"]["size"];
$tmp_file_error=  $_FILES["file"]["error"];
$tmp_pdb_file_name = $_FILES["file1"]["tmp_name"];
$tmp_txt_file_name = $_FILES["file2"]["tmp_name"];

$result=db_query("select task_status,user_id,algorithm from tasks where task_id=${task_id}");
if (!db_num_rows($result)) add_error("Task does not exist!");

$data=db_fetch_assoc($result);
$task_status=$data["task_status"];
$user_id=$data["user_id"];
$algorithm=$data["algorithm"];
db_free_result($result);

if ($user_id!=$authorized_user_id)
{
	add_error("You are not owner of this task!");
	print_error("Add data","..");
}

if (($task_status=="submitted") || 
    ($task_status=="ready") || 
    ($task_status=="stopped"))
{
	add_error("You can't modify data because the task has status '$task_status'!");
}

print_error("Upload data","..");

if ($tmp_file_error && ($fasta==""))
{
	add_error("No file was specified or upload error!");
}

if ($tmp_file_size>disk_free_space($DATA_PATH))
{
	add_error("Low free space on the server for data upload!");
}

if (($tmp_file_name!="") && ($fasta!=""))
{
	add_error("You cannot type sequences and attach files simultaniously!");
	print_error("Upload data","..");
}


//echo($tmp_file_name); 

db_query("update tasks set task_status='new',date_of_finishing=NULL  where task_id=$task_id");

$file_path="${DATA_PATH}/${user_id}/${task_id}/sequences.fasta";
$pdb_file_path="${DATA_PATH}/${user_id}/${task_id}/structure.pdb";
$txt_file_path="${DATA_PATH}/${user_id}/${task_id}/selection.txt";



$dir_name="${DATA_PATH}/${user_id}";
if (!file_exists($dir_name))
{
	if (!mkdir($dir_name))
	{
		add_error("Can't create directory '$dir_name'!");
	}
    
	chmod($dir_name,0775);

	if (!chgrp($dir_name,$LOCAL_GROUP))
	{
		add_error("Can't change group for directory '$dir_name' to the '$LOCAL_GROUP'!");
	}
}

$dir_name="${DATA_PATH}/${user_id}/${task_id}";
if (!file_exists($dir_name))
{
	if (!mkdir($dir_name))
	{
		add_error("Can't create directory '$dir_name'!");
	}

	chmod($dir_name,0775);

	if (!chgrp($dir_name,$LOCAL_GROUP))
	{
		add_error("Can't change group for directory '$dir_name' to the '$LOCAL_GROUP'!");
	}
}

print_error("Errors","..");

if ($algorithm == "nhunt")
{
	$db_set_field=array
	(
		"db_number"
	);
	read_vars($db_set_field, "post");
	$db_number=(int)$db_number;
	db_query("update tasks set db_set=$db_number  where task_id=$task_id");
}


if ($algorithm == "FitProt")
{
	//add_error("This is FitProt!");
	$flag=copy($tmp_pdb_file_name, $pdb_file_path);
	$flag=copy($tmp_txt_file_name, $txt_file_path);
	if (!chmod($pdb_file_path,0664))
	{
		add_error("Can't change permissions on file!");
	}

	if (!chgrp($pdb_file_path,$LOCAL_GROUP))
	{	
		add_error("Can't change group for file '$file_path' to the '$LOCAL_GROUP'!");
	}	
	if (!chmod($txt_file_path,0664))
	{	
		add_error("Can't change permissions on file!");
	}

	if (!chgrp($txt_file_path,$LOCAL_GROUP))
	{	
		add_error("Can't change group for file '$file_path' to the '$LOCAL_GROUP'!");
	}
}
/*
 * Check attached file
 */
else
{
if (($tmp_file_name!="") && ($fasta==""))
{
	
	$fd=fopen($tmp_file_name,"r");
	if (!$fd)
	{
		add_error("Can't open file '$tmp_file_name'!");
		print_error("Errors","..");
	}

	$character=fgetc($fd);
	while (ctype_space($character))
	{
		$character=fgetc($fd);
	}

	if($character!='>')
	{
		add_error("Bad FASTA file format!");
		print_error("Errors","..");
	}

	$flag=copy($tmp_file_name,$file_path);
	if(!$flag)
	{
		add_error("Copy file \"${tmp_file_name}\" to  \"${file_path}\" failed!");
	}
}

/*
 * Check typed sequences
 */
if (($fasta!="") && ($tmp_file_name==""))
{
    
	if ($fasta[0]!='>')
	{
		add_error("Bad FASTA file format!");
		print_error("Errors","..");
	}

	$fd=fopen($file_path,"w");
	if (!$fd)
	{
		add_error("Can't open file '$file_path'!");
		print_error("Errors","..");
	}
	fputs($fd,$fasta);
	fclose($fd);
}

if (!chmod($file_path,0664))
{
	add_error("Can't change permissions on file!");
}

if (!chgrp($file_path,$LOCAL_GROUP))
{
	add_error("Can't change group for file '$file_path' to the '$LOCAL_GROUP'!");
}
}

print_error("Errors","..");

print_refresh_page("../pages/edit_task.php?task_id=${task_id}");

?>

