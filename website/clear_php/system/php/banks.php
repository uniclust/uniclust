<?php
 /***************************************************************************************/
 function get_bank_url($databank_name)
 {
    switch($databank_name)
    {
	case "Ensembl":
	    return "http://www.ensembl.org/Homo_sapiens/";
	break;
	case "EMBL":
	    return "http://www.ebi.ac.uk";
	break;
	case "Golden Path":
	    return "http://genome.ucsc.edu";
	break;
	case "GeneBank":
	     return "http://www.ncbi.nlm.nih.gov";
	break;
    }
    return "";
 }


/****************************************************************************************/
 function genebank_id_to_url($id,$databank_name)
 {
    switch($databank_name)
    {
	case "ensembl":
	    return "http://www.ensembl.org/Homo_sapiens/geneview?gene=${id}";
	break;
    }
    return "";
 }
 /******************************************************************************************/
 function databank_id_to_url($databank_name,$chromosome,$begin,$end,$AC)
 {

    if($begin>$end)
    {
	$pos_begin=$end-1000;
	$pos_end=$begin+1000;
    }
    else
    {
	$pos_begin=$begin-1000;
	$pos_end=$end+1000;
    }
  
    switch($databank_name)
    {
	case "Golden Path":
	    return "http://genome.ucsc.edu/cgi-bin/hgTracks?position=chr${chromosome}%3A${pos_begin}-${pos_end}";
	break;
	case "Ensembl":
	    return "http://www.ensembl.org/Homo_sapiens/cytoview?chr=${chromosome}&vc_start=${pos_begin}&vc_end=${pos_end}";
	break;
	case "GeneBank":
	    return "http://www.ncbi.nlm.nih.gov/entrez/viewer.fcgi?val=${AC}";
	break;
	case "EMBL":
	    return "http://www.ebi.ac.uk/cgi-bin/emblfetch?style=html&id=${AC}&Submit=Go";
	break;
    }
    
    return "";
    
 }
/******************************************************************************************************/
?>
