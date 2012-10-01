<?

 $base_dir="../system/php";

 require_once("../etc/global_variables.php");
 require_once($base_dir."/page.php");
 require_once($base_dir."/tables.php");
 require_once($base_dir."/forms.php");

 print_page_header("Multiple sequence alignment on multiprocessors",".");
 
 $htpps_host_with_site_path=$HTTPS_HOST;
 if ($SITE_PATH!="") $htpps_host_with_site_path.="/".$SITE_PATH;
?>
  <p style="text-align:left"><font size="+1"><b>Introduction</b></font></p>
  
  <font face="arial">
  <P style="text-align:justify">
	Welcome to the <ins>Multiple Sequence Alignment on Multiprocessors!</ins><br>
	This site allows the user to align DNA/RNA or amino acid sequences, using one of the available 
	multiprocessor systems. It provides an interface to create tasks, attach data in the 
	<a href="http://en.wikipedia.org/wiki/Fasta_format">FASTA format</a>
	to each task and then submit it for execution. The server script analyzes
	user's task content, then transfers the data to one of the multiprocessors and submit the task
	to the remote execution queue. The system transfers the data from finished tasks to the user 
	directory by the use of periodic check for existing data.
	And then the user will receive an email informing that the processing of his task is done or rejected.<br></br>
	You should <? print("<A href=\"https://$htpps_host_with_site_path/pages/create_user.php\">register</A>"); ?> 
	to use the multiprocessor system. Or, if you already have an account on this website, visit your 
	<? print("<A href=\"https://$htpps_host_with_site_path/pages/main.php\">personal user page</A>"); ?>.
  </P>
  </font>

  <p style="text-align:left"><font size="+1"><b>Algorithms</b></font></p>
  <font face="arial">
  <P style="text-align:justify">
	The current version of alignment tools on the website uses the modified MUSCLE algorithm. 
	Sources and documentation for the MUSCLE are available at 
	<A href="http://www.drive5.com/muscle">http://www.drive5.com/muscle</a>. 
	The modification was intended to adaptize MUSCLE algorithm for parallel computing
	by means of PARUS system, which is available at 
	<A href="http://parus.sourceforge.net">http://parus.sf.net</A>.  	
  </P>
  </font>

  <p style="text-align:left"><font size="+1"><b>References</b></font></p>
  
<?
	print_table_header();
		print_view_table_row
		(
			array
			(
				"<center style=\"text-align:left\"> <font size=\"+1\" face=\"times new roman\" color=\"darkgreen\">
					<I>Alexey N. Salnikov</I> The modification of MUSCLE multiple
					sequence alignment algorithm for multiprocessors 
					Proceedings of the 3-rd Moscow conference on computational
					molecular biology, Moscow, Russia, July 27-31 2007, pp. 
					270-271.
				</font></center>"
            ),
            False
		);
		print_view_table_row
		(
			array
			(
				"<center  style=\"text-align:left\"> <font size=\"+1\" face=\"times new roman\" color=\"darkgreen\">
					<I>Alexey N. Salnikov</I> PARUS: \"A Parallel Programming Framework for
					Heterogeneous Multiprocessor Systems\" Lecture Notes in 
					Computer Science  (LNCS 4192) Recent Advantages 
					in Parallel Virtual Machine and Message Passing Interface,
					Volume 4192,  pp. 408-409, 2006,  ISBN-10: 3-540-39110-X 
					ISBN-13: 978-3-540-39110-4.
					<a href=\"http://dx.doi.org/10.1007/11846802_59\">Link</a>
				 </font></center>"
             ),
             False
		);

	print_table_tail();
?>

</body>
</html>

