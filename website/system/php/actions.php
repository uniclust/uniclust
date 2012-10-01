<?
function get_action_string($action_name,$action,$base_path,$label)
{
    $str ="\t\t<A href=\"${action}\" >";
    $str.="\t\t\t<IMG src=\"${base_path}/images/buttons/actions/${action_name}.png\"";
    $str.="\t\t\t\talt=\"${label}\"";
    $str.="\t\t\t\tborder=\"0\"";
    $str.="\t\t\t\theight=\"25\"";
    $str.="\t\t\t\twidth=\"60\"";
    $str.="\t\t\t>";
    $str.="\t\t</A>";
    
    return $str;
}
?>
