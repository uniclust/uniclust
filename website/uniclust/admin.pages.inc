<?php
function adminpage_uniclust_callback(&$form = NULL, &$form_state = NULL) 
{
	$current_user = getFullUniclustUserInfo();
	if($current_user['id']==0 || $current_user['id_rights'] != 1 || !CheckDrupalEntityKey()) drupal_access_denied();//drupal_not_found();
	$page['static_content'] = array('#markup'=>'<p>Здравствуйте, Руковолитель группы UNICLUST!</p>');
	$page['reg_new_user_form'] = drupal_get_form('registrate_new_uniclust_user_form');
	$page['exit_form'] = drupal_get_form('unbind_account_form');
	
	return $page;
}

//форма для регистрации нового пользователя админом в UNICLUST
function registrate_new_uniclust_user_form()
{
	$form['password'] = array(
		'#type' => 'textfield', //you can find a list of available types in the form api
		'#title' => t('Пароль:'),
		'#size' => 25,
		'#maxlength' => 25,
	  );
	 $form['email'] = array(
		'#type' => 'textfield', //you can find a list of available types in the form api
		'#title' => t('E-mail:'),
		'#size' => 25,
		'#maxlength' => 50,
		'#required' => TRUE, //make this field required 
	  );
	  $form['full_username'] = array(
		'#type' => 'textfield', //you can find a list of available types in the form api
		'#title' => t('Полное имя пользователя:'),
		'#size' => 25,
		'#maxlength' => 30,
	  );
	$form['rights_select'] = array(
       '#type' => 'select',
       '#title' => t('Права доступа:'),
       '#options' => array(
       ),
       //'#default_value' => $category['selected'],
       '#description' => t('Set this to choice rights of the new user.'),
      );
	$form['submit_button'] = array(
		'#type' => 'submit',
		'#value' => t('Зарегистрировать'),
	  );
	$link = get_db_connection();
	//$query ="INSERT INTO `uniclust_users` (`uniclust_users_id`, `login`, `email`, `password`, `full_user_name`, `date_of_registration`, `priority_tokens`, `id_rights`, `id_cms_user`) VALUES (NULL,'".$form_state['values']['login']."','".$form_state['values']['email']."','".get_password_hash($form_state['values']['password'])."','".$form_state['values']['full_username']."','".time()."',1,2,-1);";
	$query = "SELECT * FROM `rights`";
	$result = mysqli_query($link, $query) or die("Ошибка выполнения запроса" . mysqli_error($link));
	mysqli_close($link);
	if($result)
	{
		$row_cnt = mysqli_num_rows($result);
		mysqli_data_seek($result,0);
		while($row = mysqli_fetch_assoc($result))
		{
			$form['rights_select']['#options'][$row['rights_id']] = $row['right'];
		}
	}
	return $form;
}

function registrate_new_uniclust_user_form_validate($form, &$form_state)
{
	$fields_filled = TRUE;
	if(!isset($form_state['values']['email']))
	{
		$fields_filled = FALSE;
	}
	if(!$fields_filled)
	{
		form_set_error(array('password','email'), t('Заполните все обязательные поля!'));
	}
}

function registrate_new_uniclust_user_form_submit($form, &$form_state)
{
	//проверим ключ сущности Drupal
	$key = CheckDrupalEntityKey();
	if(!$key)
	{
		form_set_error('login', 'В вашей сущности Drupal используется неккоректный ключ. Введите корректный ключ в настройках модуля UNICLUST и повторите попытку.');
		return;
	}
	//вызовем хранимую процедуру для создания нового аккаунта
	$link = get_db_connection();
	$query ="call `test_7`('".$form_state['values']['email']."', 1, ".$form_state['values']['rights_select'].", '".$form_state['values']['password']."', '".$key."')";
	$result = mysqli_query($link, $query);// or die("Ошибка выполнения запроса" . mysqli_error($link));
	mysqli_close($link);
	if($result)
	{
		$row = mysqli_fetch_array($result);
		drupal_mail('system', 'mail', $row['email'], language_default(), array(
		  'context' => array(
			'subject' => 'Создан аккаунт UNICLUST',
			'message' => 'Здравствуйте! В системе UNICLUST был создан аккаунт с данным почтовым ящиком. Логин: '.$row['login'].'. Пароль: '.$row['password'].'. С уважением администрация UNICLUST!',
		  )
		));
		drupal_set_message("Новый пользователь был добавлен в базу данных.<br/>Письмо с данными аккаунта было отправлено на указанный почтовый ящик.<br />Запомните пароль, т.к. в таком виде он больше нигде не покажется.<br /> Логин:".$row['login']."<br />Пароль:".$row['password']."<br />E-mail:".$row['email']."<br />Права доступа:".$form_state['values']['rights_select']);
	}
	else
	{
		form_set_error('submit', t("По каким-то причинам не удалось добавить нового пользователя в базу данных (возможно данный почтовый ящик уже занят). Повторите позже."));
	}
}