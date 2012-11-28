<?

 $base_dir="../system/php";

 require_once("../etc/global_variables.php");
 require_once($base_dir."/page.php");
 require_once($base_dir."/tables.php");
 require_once($base_dir."/forms.php");

 print_page_header("Rational protein design on multiprocessors",".");
 
 $htpps_host_with_site_path=$HTTPS_HOST;
 if ($SITE_PATH!="") $htpps_host_with_site_path.="/".$SITE_PATH;
?>
  <p style="text-align:left"><font size="+1"><b>Introduction</b></font></p>
  
  <font face="arial">
  <P style="text-align:justify">
	Welcome to the <ins>Rational protein design on Multiprocessors!</ins><br>
	This site allows the user to design proteins, using one of the available 
	multiprocessor systems. It provides an interface to create tasks, attach data in the 
	<a href="http://en.wikipedia.org/wiki/Protein_Data_Bank_(file_format)">PDB format</a> and text file with information about design positions
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
	The current version of design tools on the website uses the modified version
	of FITPROT algorithm described in the first reference. The modification was 
	intended to adaptize FITPROT algorithm for parallel computing by means of MPI library.
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
					<I>Grishin A., Fonfara I., Wende W., Alexeyevsky D., Alexeevski A., Spirin S., Zanegina O., Karyagina A.</I> Bioinformatics analysis of LAGLIDADG homing endonucleases for construction of enzymes with changed DNA recognition specificity. 4-th Moscow Conference on Computational Molecular Biology, 2009, Moscow, MSU, p.123.
					
				</font></center>"
            ),
            False
		);
		print_view_table_row
		(
			array
			(
				"<center  style=\"text-align:left\"> <font size=\"+1\" face=\"times new roman\" color=\"darkgreen\">
					<I>Voigt CA., Gordon DB., Mayo SL.</I> Trading accuracy for speed: A quantitative comparison of search algorithms in protein sequence design. J Mol Biol. 2000 Jun 9;299(3):789-803. PubMed PMID: 10835284.
				 </font></center>"
             ),
             False
		);

	print_table_tail();
?>

</body>
</html>

