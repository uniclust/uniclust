<?php
require_once("sequence.php");
require_once("actions.php");

/***********************************************************************************/
function print_view_table_header($names,$comment,$filter=True)
{
?>

  <P>
   <DIV class="table_comment">
<?php
	printf("%s<br></br>",$comment);
?>
   </DIV>
   <TABLE border="">
<?php
	if ($names!="")
	{
		printf("<TR>");
		$num_names=count($names);
		for ($i=0;$i<$num_names;$i++)
		{
            printf("<TH class=\"general\">");
            if($filter)
            {
                printf("   &nbsp;%s&nbsp;",htmlspecialchars($names[$i]));
            }
            else
            {
                printf("   &nbsp;%s&nbsp;",$names[$i]);
            }
			printf("</TH>");
		}
		printf("</TR>");
	}
}
/************************************************************************************/
function print_view_table_row($data,$filter=True)
{
?>
    <TR>
<?php
	$num_data=count($data);
	for($i=0;$i<$num_data;$i++)
	{
		printf("<TD class=\"general\">");
		if ($data[$i]=="")
			printf("&nbsp;");
        else
        {
           $str=stripslashes($data[$i]);
           if($filter)
           {
                $str=htmlspecialchars($str);
           }
           printf("&nbsp;%s&nbsp;",$str);
        }
		printf("</TD>");
	}
									
?>
    </TR>
   
<?php
}
/************************************************************************************/
function print_view_table_tail()
{
?>
  
   </TABLE>
  </P>
  
<?php
}
/***********************************************************************************/
function print_action_table_header()
{
?>
  <P>
   <TABLE>
    <TR>
<?php
}
/**********************************************************************************/
function print_action_table_command($command_name,$action,$base,$label)
{
	printf("<TD class=\"general\">");
	printf("%s",get_action_string($command_name,$action,$base,$label));
	printf("</TD>");
}
/**********************************************************************************/
function print_action_table_tail()
{
?>
    </TR>
   </TABLE>
  </P>
  
<?php
}
?>
