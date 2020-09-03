<?php

require_once("sequence.php");


/************************************************************************************/
function print_null_input($value,$comment,$filter=True)
{
?>
 <TR>
  <TD class="general">
<?php
    $value=stripslashes($value);
    if($filter) $value=htmlspecialchars($value);
	if ($value=="")
		printf("&nbsp;");
	else
		printf("<B><I>&nbsp;%s&nbsp;</I></B>",$value);
?>
  </TD>
  <TD class="general">
<?php
	printf("&nbsp;%s&nbsp;",$comment);
?>
  </TD>
 </TR>
 
<?php
	return;
}
/************************************************************************************/
function print_file_input($name,$comment)
{
?>
 <TR>
  <TD class="general">
<?php
	printf("<INPUT type=\"file\" name=\"%s\">",$name);
?>
  </TD>
  <TD class="general">
<?php
	printf("&nbsp;%s&nbsp;",$comment);
?>
  </TD>
 </TR>
 
<?php
	return;

}

/************************************************************************************/
function print_text_input($name,$value,$comment,$filter=True)
{

    $value=stripslashes($value);
    if($filter) $value=htmlspecialchars($value);

?>
 <TR>
  <TD class="general">
<?php
	printf("<INPUT type=\"text\" name=\"%s\" value=\"%s\" width=\"100%%\" style=\"text-align:center\">",$name,$value);
?>
  </TD>
  <TD class="general">
<?php
	printf("&nbsp;%s&nbsp;",$comment);
?>
  </TD>
 </TR>
 
<?php
	return;
}
/************************************************************************************/
function print_password_input($name,$value,$comment,$filter=True)
{

    $value=stripslashes($value);
    if($filter) $value=htmlspecialchars($value);

?>
 <TR>
  <TD class="general">
<?php
	printf("<INPUT type=\"password\" name=\"%s\" value=\"%s\" width=\"100%%\" style=\"text-align:center\">",$name,$value);
?>
  </TD>
  <TD class="general">
<?php
	printf("&nbsp;%s&nbsp;",$comment);
?>
  </TD>
 </TR>
 
<?php
	return;
}
/***********************************************************************************/
function print_checkbox_input($name,$value,$checked,$comment,$filter=True)
{
// It looks like a small square in a huge table cell :)
    $value=stripslashes($value);
    if($filter) $value=htmlspecialchars($value);

?>
 <TR>
  <TD class="general">
<?php
	if ($checked=="yes")
		printf("<INPUT type=\"checkbox\" name=\"%s\" value=\"%s\" checked>",$name,$value);
	else
		printf("<INPUT type=\"checkbox\" name=\"%s\" value=\"%s\">",$name,$value);
?>
  </TD>
  <TD class="general">
<?php
	printf("&nbsp;%s&nbsp;",$comment);
?>
  </TD>
 </TR>

<?php
	return;
}
/***********************************************************************************/
function print_radio_input($var,$values,$names,$checked_value,$comment,$filter=True)
{
?>
 <TR>
  <TD>
<?php
	$item_num=count($names);
	if (($item_num>0) && ($item_num==count($values)))
	{
		for ($i=0; ($i<$item_num) && ($values[$i]!=$checked_value); $i++)
        {
            $str=stripslashes($values[$i]);
            if($filter) $str=htmlspecialchars($str);
			printf("<INPUT type=\"radio\" name=\"%s\" value=\"%s\" style=\"text-align:left\">",$var,$str);
			print("&nbsp;$names[$i]&nbsp;<br>");
        }
        
        $str=stripslashes($values[$i]);
        if($filter) $str=htmlspecialchars($str);
		printf("<INPUT type=\"radio\" name=\"%s\" value=\"%s\" style=\"text-align:left\" checked>",$var,$str);
		print("&nbsp;${names[$i]}&nbsp;<br>");
		for ($i=$i+1; $i<$item_num; $i++)
        {
            $str=stripslashes($values[$i]);
            if($filter) $str=htmlspecialchars($str);
			printf("<INPUT type=\"radio\" name=\"%s\" value=\"%s\" style=\"text-align:left\">",$var,$str);
			print("&nbsp;$names[$i]&nbsp;<br>");
		}
	}
?>
  </TD>
  <TD class="general">
<?php
	printf("&nbsp;%s&nbsp;",$comment);
?>
  </TD>
 </TR>

<?php
	return;
}
/************************************************************************************/
function print_textarea_input($name,$value,$comment,$filter=True)
{

    $value=stripslashes($value);
    if($filter) $value=$value=htmlspecialchars($value);

?>
 <TR>
  <TD class="general">
<?php
	printf("<TEXTAREA name=\"%s\" rows=\"10\" cols=\"66\">",$name);
	printf("%s",$value);
?>
</TEXTAREA>
  </TD>
  <TD class="general">
<?php
	printf("&nbsp;%s&nbsp;",$comment);
?>
  </TD>
 </TR>
 
<?php
	return;

}
/*************************************************************************************/
function print_sequence_input($name,$sequence,$comment)
{
	$sequence=stripslashes($sequence);
	$sequence=format_sequence($sequence);

?>
 <TR>
  <TD class="general">
<?php
	printf("<TEXTAREA name=\"%s\" rows=\"10\" cols=\"66\">",$name);
	printf("%s",$sequence);
?>
</TEXTAREA>
  </TD>
  <TD class="general">
<?php
	printf("&nbsp;%s&nbsp;",$comment);
?>
  </TD>
 </TR>
 
<?php
	return;

}
/*************************************************************************************/
function print_select_input($name,$lables,$values, $default_value, $comment,$filter=True)
{
	$num_lables=count($lables);

    if($filter) $default_value=htmlspecialchars($default_value);

	for ($def_val_indx=0; ($def_val_indx<$num_lables) && (($values[$def_val_indx]!=$default_value)); $def_val_indx++) ;
?>

 <TR>
   <TD class="general">
<?php
	printf("<SELECT name=\"%s\">",$name);
	
	if ($def_val_indx<$num_lables)
    {
        if($filter) $def_lable=htmlspecialchars($lables[$def_val_indx]);
		printf("<OPTION value=\"%s\" >%s</OPTION>",$default_value,$def_lable);
		
        for ($i=0; $i<$def_val_indx; $i++)
        {

            if($filter)
            {
                $l=htmlspecialchars($lables[$i]);
                $v=htmlspecialchars($values[$i]);
            }
            else
            {
                $l=$lables[$i];
                $v=$values[$i];
            }
            printf("<OPTION value=\"%s\" >%s</OPTION>",$v,$l);
        }
        for ($i=$def_val_indx+1; $i<$num_lables; $i++)
        {
 
            if($filter)
            {
                $l=htmlspecialchars($lables[$i]);
                $v=htmlspecialchars($values[$i]);
            }
            else
            {
                $l=$lables[$i];
                $v=$values[$i];
            }
            printf("<OPTION value=\"%s\" >%s</OPTION>",$v,$l);
           
        }
	}
	else
	{
        for ($i=0; $i<$num_lables; $i++)
        {
  
            if($filter)
            {
                $l=htmlspecialchars($lables[$i]);
                $v=htmlspecialchars($values[$i]);
            }
            else
            {
                $l=$lables[$i];
                $v=$values[$i];
            }
            printf("<OPTION value=\"%s\" >%s</OPTION>",$v,$l);
         
        }
	}
	printf("</SELECT>");
?>
   </TD>
  <TD class="general">
<?php
	printf("&nbsp;%s&nbsp;",$comment);
?>
  </TD>
 </TR>
 
<?php
	return;
}
/*************************************************************************************/
function print_hidden_input($name,$value,$filter=True)
{
    $value=stripslashes($value);
    if($filter) $value=htmlspecialchars($value);
	printf("<INPUT type=\"hidden\" name=\"%s\" value=\"%s\">",$name,$value);
}
/*************************************************************************************/
function print_submit_input($name,$text)
{
?>
  
  <P>
   <CENTER>
<?php
	printf("<INPUT type=\"submit\" name=\"%s\" value=\"%s\">",$name,$text);
?>
   </CENTER>
  </P>

<?php
}
/*************************************************************************************/
function print_genome_location_input($chr,$band_0,$band_1,$band_2,$band_3)
{

	$band_1=stripslashes($band_1);
	$band_2=stripslashes($band_2);
	$band_3=stripslashes($band_3);

?>
  <P>
   <DIV class="genome_location">
    Location in genome
   </DIV>
  </P>
  
<?php
	print_table_header();

	$chromosomes=array
	(
		"",
		"1",
		"2",
		"3",
		"4",
		"5",
		"6",
		"7",
		"8",
		"9",
		"10",
		"11",
		"12",
		"13",
		"14",
		"15",
		"16",
		"17",
		"18",
		"19",
		"20",
		"21",
		"22",
		"X",
		"Y"
	);

	print_select_input
	(
		"chromosome",
		$chromosomes,
		$chromosomes,
		$chr,
		"Please select a Chromosome."
	);

	print_table_tail();

?>

  <P>
   <DIV class="genome_location">
     Location in the chromosome
   </DIV>
  </P>
  
<?php

	print_table_header();
?>
  <TR>
  <TD class="general">
  <TABLE>
  <TR>
<?php
	
	if($band_0=="q")
	{
?>
     <TD class="general">
      <SELECT name="band_0">
        <OPTION value="q">q</OPTION>
        <OPTION value="p">p</OPTION>
        <OPTION value=""></OPTION>
      </SELECT>
     </TD>
<?php
	}
	
	if($band_0=="p")
	{
?>
     <TD class="general">
      <SELECT name="band_0">
        <OPTION value="p">p</OPTION>
        <OPTION value="q">q</OPTION>
        <OPTION value=""></OPTION>
      </SELECT>
     </TD>
<?php
	}
	
	if($band_0=="")
	{
?>
     <TD class="general">
      <SELECT name="band_0">
        <OPTION value=""></OPTION>
        <OPTION value="p">p</OPTION>
        <OPTION value="q">q</OPTION>
      </SELECT>
     </TD>

<?php
	}
?>
     
     <TD class="general">.</TD>
     
     <TD class="general">
        <INPUT
	   type="text"
	   name="band_1"
	   size="6"
	   maxlength="6"
<?php
	printf("value=\"%s\"",$band_1);
?>
	>
     </TD>
     
     <TD class="general">.</TD>
     
     <TD class="general">
        <INPUT
	   type="text"
	   name="band_2"
	   size="6"
	   maxlength="6"
<?php
	printf("value=\"%s\"",$band_2);
?>
	>
     </TD>

     <TD class="general">.</TD>
     
     <TD class="general">
        <INPUT
	   type="text"
	   name="band_3"
	   size="6"
	   maxlength="6"
<?php
	printf("value=\"%s\"",$band_3);
?>
	>
     </TD>
  </TR>
  </TABLE>
  </TD>
  </TR>

<?php
	print_table_tail();
}
/*************************************************************************************/
function print_form_header($name,$action)
{
	printf("<FORM name=\"%s\" action=\"%s\" method=\"post\">",$name,$action);
}
/*************************************************************************************/
function print_form_tail()
{
	print("</FORM>");
}
/*************************************************************************************/
function print_file_form_header($name,$action)
{
	printf("<FORM name=\"%s\" enctype=\"multipart/form-data\" action=\"%s\" method=\"post\">",$name,$action);
}
/*************************************************************************************/
function print_file_form_tail()
{
	print_form_tail();
}
/*************************************************************************************/
function print_table_header()
{
?>
  
  <P>
  <TABLE border="">

<?php
}
/************************************************************************************/
function print_table_header_name($comment)
{
?>
  
  <P>
  <TABLE border="">

   <DIV class="table_comment">
<?php
	printf("&nbsp;%s&nbsp;",$comment);
?>
   </DIV>
  
<?php
}

/************************************************************************************/
function print_table_tail()
{
?>
  
  </TABLE>
  </P>
  
<?php
}
/***********************************************************************************/
function print_main_table_button($name,$status_button,$base)
{
	$lower_name=strtolower($name);
?>
 <TR>
  <TD>
<?php
	if($status_button=="unpushed")
		printf("<A href=\"main.php?table=%s\">",$name);
    
	printf("<IMG src=\"%s/images/buttons/objects/%s_%s.gif\"",$base,$lower_name,$status_button);
	printf("     alt=\"%s %s button\"",$name,$status_button);
?>
        border="0"
        height="50"
        width="150"
     >
<?php
	if($status_button=="unpushed")
		printf("</A>");
?>
  </TD>
 </TR> 
<?php
}
/************************************************************************************/

?>
