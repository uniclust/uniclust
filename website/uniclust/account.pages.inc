<?php
//Страница личного кабинета
function account_uniclust_callback($form = NULL, &$form_state = NULL) {
	$uniclust_user = getFullUniclustUserInfo();
	if($uniclust_user['id']==0) header("Location:".url('uniclust/',array('absolute'=>true)));
	if($uniclust_user['id_rights'] == 1)
	{
		$page['admin_panel_link'] = array('#markup' => '<a href="'.url('uniclust/admin',array('absolute'=>true)).'">Перейти в Панель администратора</a><br>');
	}
	$page['account_info'] = array('#markup' => 'Здравствуйте, '.$uniclust_user['full_user_name'].'!<br />Ваш логин: '.$uniclust_user['login'].'<br />Ваш e-mail: '.$uniclust_user['email'].'<br />Ваш аккаунт зарегистрирован: '.$uniclust_user['date_of_registration'].'<br />');
	$page['change_password_header'] = array('#markup' =>'<br /><h2>Смена пароля</h2><br />');
	$page['change_password_form'] = drupal_get_form('change_password_form');
	
	$page['change_password_form']['new_password']['pass1']['#title'] = 'Новый пароль';
	$page['change_password_form']['new_password']['pass2']['#title'] = 'Повторите новый пароль';
	return $page;
}

//форма для смены пароля
function change_password_form()
{
	$form['password'] = array(
		'#type' => 'password', //you can find a list of available types in the form api
		'#title' => 'Старый пароль:',
		'#size' => 30,
		'#maxlength' => 30,
		'#required' => TRUE, //make this field required 
	  );
	$form['new_password'] = array(
		'#type' => 'password_confirm', //you can find a list of available types in the form api
		//'#title' => 'Новый пароль:',
		'#size' => 30,
		'#maxlength' => 30,
		'#required' => TRUE, //make this field required
	  );
	//$form['new_password']['pass1']['#title'] = 'Новый пароль ёпта';
	$form['submit_button'] = array(
		'#type' => 'submit',
		'#value' => t('Сменить пароль'),
	  );
	 
	return $form;
}

function change_password_form_validate($form, &$form_state)
{
	$uniclust_user = getFullUniclustUserInfo();
	$key = CheckDrupalEntityKey();
	//!!!!!!!!!!!!!ещё нужно проверять, что данный пользователь uniclust принадлежит сущности Друпал именно с таким ключом $key!
	
	if($uniclust_user['id']==0 || !$key) form_set_error('password','Чтобы изменить пароль учётной записи UNICLUST, в неё сначала нужно <a href="'.url('uniclust',array('absolute'=>true)).'" >войти!</a>');
	if(strlen($form_state['values']['new_password']) < 8)
	{
		form_set_error('new_password',t('Минимальная длина пароля должна быть не менее 8ми символов.'));
	}
	if(get_password_hash($form_state['values']['password']) != $uniclust_user['password_hash'])
	{
		form_set_error('password', 'Вы ввели неверный пароль от данной учётной записи!');
	}
}

function change_password_form_submit($form, &$form_state)
{
	$uniclust_user = getFullUniclustUserInfo();
	$link = get_db_connection();
	$query ="UPDATE uniclust_users SET password ='".get_password_hash($form_state['values']['new_password'])."' WHERE uniclust_users.uniclust_users_id = ".$uniclust_user['id'];
	$result = mysqli_query($link, $query) or die("Ошибка выполнения запроса" . mysqli_error($link));
	if(mysqli_affected_rows($link)==1)
	{
		drupal_set_message("Пароль был успешно изменён!");
		drupal_mail('system', 'mail', $uniclust_user['email'], language_default(), array(
		  'context' => array(
			'subject' => 'Изменён пароль UNICLUST',
			'message' => 'Здравствуйте! Пароль к Вашему аккаунту UNICLUST был успешно изменён. Если Вы этого не делали, но получили это письмо - свяжитесь с администратором UNICLUST. С уважением администрация UNICLUST!',
		  )
		));
	}
	else
	{
		form_set_error('submit', t("По каким-то причинам не удалось изменить пароль. Повторите позже."));
	}
	mysqli_close($link);
}