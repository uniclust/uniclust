<?

 $base_dir="../../system/php";

 require_once($base_dir."/page.php");
 require_once($base_dir."/forms.php");
 
 require_once("../../etc/global_variables.php");
 
 print_page_header("New user registration","..");
?>

 <P>
  To create an account you should type your full name, email address and login.
  After that you will receive an email with confirmation link. Click on it and
  the registration will be done and you will be asked to set a password.
 </P>

<?
 printf(" <P><A href=\"http://$HTTP_HOST/$SITE_PATH\">Go to the root page</A></P>");

 print_form_header("auth","../queries/create_user.php");
 print_table_header();
    print_text_input("user_name","","Full name");
    print_text_input("login","","Desired login");
    print_text_input("email","","Email address");
 print_table_tail();
 print_submit_input("auth","Create user");
 print_form_tail();

?>

</body>
</html>

