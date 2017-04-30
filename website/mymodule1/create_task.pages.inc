<?php
function create_task_uniclust_callback(&$form = NULL, &$form_state = NULL) 
{
	$current_user = getFullUniclustUserInfo();
	if($current_user['id'] == 0) drupal_access_denied();//drupal_not_found();
	$page['static_content'] = array('#markup'=>'<p>Здравствуйте! На этой странице Вы можете создать новую задачу для выполнения на суперкомпьютере!</p>');
	return $page;
}
