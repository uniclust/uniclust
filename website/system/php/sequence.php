<?php
 /**************************************************************************/
 function format_sequence($seq)
 {
  $res=chunk_split($seq,10,' ');
  return $res;
 }
 /**************************************************************************/
 function sequence_right_test($seq)
 {
  $res=ereg_replace("[atgcswrykmbvhdn\-\.~[:space:]\t\n]","",$seq);
  if($res!="") return 0;
  return 1;
 }
 /**************************************************************************/
 function sequence_clear($seq)
 {
  $res=ereg_replace("[\-\.~[:space:]\t\n]","",$seq);
  return strtolower($res);
 } 
 /**************************************************************************/
 function sequence_show($seq)
 {
 ?> 
  <FONT face="courier">
  <TABLE>
 <?php
  $len=strlen($seq);
  $j=0;
  $k=0;
  for($i=0;$i<$len;$i++)
  {
   if(($j==0)&&($k==0))
   {
    printf("<TR>\n");
   }
   if($k==0)
   {
    printf("<TD>\n");
   }
   echo($seq[$i]);
   if($k==9)
   {
    printf("</TD>\n");
    $j++;
    $k=-1;
   }
   if($j==6)
   {
    printf("</TR>\n");
    $j=0;
   }
   $k++;
  }
?>
</TABLE>
</FONT>
<?php
 }
/***********************************************************************************/
function sequence_compare($begin,$end,$full_sequence,$sequence)
{
 //echo "sequence_compare(".$begin.",".$end.",".$full_sequence.",".$sequence.")\n\n";
 echo "\nsequence_compare(".$begin.",".$end.",".full_sequence.",".sequence.")\n\n";
 $tmp_seq=substr($full_sequence,$begin,$end-$begin+1);
 
 echo "(forward-full)"."${tmp_seq}\n";
 echo "(forward-----)"."${sequence}\n";
 echo "(reverce-full)".sequence_rev($tmp_seq)."\n";
 echo "--".strlen($tmp_seq)."--".strlen($sequence)."\n";
 
 //return sequence_native_compare($tmp_seq,$sequence);
 
 
 $flag=strcasecmp($tmp_seq,$sequence);

 //echo "--".$tmp_seq."--".$sequence."--\n";
 //echo "--".strlen($tmp_seq)."--".strlen($sequence)."\n";

 if($flag==0)
 {
  return 1;
 }
 else
 {
  return 0;
 }
}
/**********************************************************************************/
function sequence_rev($sequence)
{
 $result="";
 
 for($i=strlen($sequence)-1;$i>=0;$i--)
 {
  $val=$sequence[$i];
  //echo "sequence[${i}]==${val}";
  switch($val)
  {
   case 'a':
    $val='t';
   break;
   case 't':
    $val='a';
   break;
   case 'g':
    $val='c';
   break;
   case 'c':
    $val='g';
   break;
   case 'r':
    $val='y';
   break;
   case 'y':
    $val='r';
   break;
   case 'm':
    $val='k';
   break;
   case 'k':
    $val='m';
   break;
   case 's':
    $val='s';
   break;
   case 'w':
    $val='w';
   break;
   case 'h':
    $val='d';
   break;
   case 'b':
    $val='v';
   break;
   case 'v':
    $val='b';
   break;
   case 'd':
    $val='h';
   break;
   case 'n':
    $val='n';
   break;
   default:
    printf("Unexpected symbol in original ( not reversed ) sequence \n");
    return -1;
   break;
  }
  $result=$result."${val}";
 }
 //echo "(--${sequence}--)\n";
 return $result;
}
/**********************************************************************************/
function sequence_native_compare($seq1,$seq2)
{
 
    //echo "--".$seq1."--".$seq2."--\n";
    //echo "--".strlen($seq1)."--".strlen($seq2)."\n";

 $len=strlen($seq1);
 if($len!=strlen($seq2)) return 0;
 
 
 
 for($i=0;$i<$len;$i++)
 {
  if(($seq1[$i]!='a')&&($seq1[$i]!='t')&&($seq1[$i]!='g')&&($seq1[$i]!='c'))
  {
   if(($seq2[$i]=='a')||($seq2[$i]=='t')||($seq2[$i]=='g')||($seq2[$i]=='c')) return 0;
  }
  switch($seq1[$i])
  {
   case 'a':
   break;
    if($seq2[$i]!='a') return 0;
   case 't':
    if($seq2[$i]!='t') return 0;
   break;
   case 'g':
    if($seq2[$i]!='g') return 0;
   break;
   case 'c':
     if($seq2[$i]!='c') return 0;
   break;
  }
 }
 return 1;
}

/**********************************************************************************/
?>
