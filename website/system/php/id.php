<?php

function get_and_increment_id($lock_name,$barrier,$base)
{
	$id=file($base."/locks/".$lock_name.".lock");
	$id_val=$id[0];
	
	$fd=fopen($base."/locks/".$lock_name.".lock","w");
	if ($id_val>=$barrier)
	{
		fputs($fd,"0");
	}
	else
	{
		fputs($fd,$id_val+1);
	}

	return $id_val;
}

?>

