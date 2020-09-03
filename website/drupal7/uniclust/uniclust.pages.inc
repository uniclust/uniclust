<?php
//Главная страница UNICLUST
function mainpage_uniclust_callback($form = NULL, &$form_state = NULL) {
	$uniclust_user = getFullUniclustUserInfo();
	//проверим, авторизован ли вообще пользователь
	if($uniclust_user['id']==0) header("Location:".url('uniclust/',array('absolute'=>true)));
	if(!CheckDrupalEntityKey())
	{
		drupal_set_message('В данной сущности Drupal используется неккоректный ключ сущности. Обратитесь к администратору данной сущности Drupal.' ,'error');
		return array();
	}
	if($uniclust_user['id_rights']==1)
	{
		$page['admin_panel_link'] = array('#markup' => '<a href="'.url('uniclust/admin',array('absolute'=>true)).'">Перейти в Панель администратора</a><br />');
	}
	$page['create_new_task_link'] = array('#markup' => '<a href="'.url('uniclust/create_task',array('absolute'=>true)).'">Создать новую задачу</a><br />');
	$page['files_link'] = array('#markup' => '<a href="'.url('uniclust/files',array('absolute'=>true)).'">Перейти на страницу работы с файлами</a><br />');
	$page['account_link'] = array('#markup' => '<a href="'.url('uniclust/account',array('absolute'=>true)).'">Перейти в личный кабинет</a><br />');
	$page['unbind_btn_form'] = drupal_get_form('unbind_account_form');
	return $page;
}



//Кнопка для перехода на страницу для создания новой задачи
function new_task_uniclust_form() 
{
	if(getFullUniclustUserInfo()['id']==0) header("Location:".url('uniclust/',array('absolute'=>true)));
	$form['submit_button'] = array(
		'#type' => 'submit',
		'#value' => t('Создать новую задачу'),
	  );
	return $form;
}
function new_task_uniclust_form_submit($form, &$form_state)
{
	form_set_error('edit-submit-button','Страница для создания задачи ещё не создана!');
	header("Location:".url('',array('absolute'=>true)));
}