<?php

//страница для авторизации
function authorization_page_callback($form = NULL, &$form_state = NULL) 
{
	if(getFullUniclustUserInfo()['id']!=0) header("Location:".url('uniclust/workspace',array('absolute'=>true)));
	$page['static_content'] = array('#markup'=>'<p>Войдите в систему UNICLUST<br>Если вы уже входили, то введите данные, которые использовали в последний раз. Иначе введите данные свободной учётной записи UNICLUST (обычно выдаётся руководителем группы) для её привязки к Вашему аккаунту на сайте.</p>');
	$page['enter_form'] = drupal_get_form('authorization_form');
	return $page;
}

//форма авторизации
function authorization_form($form, &$form_state) 
{
	$form['login_or_email'] = array(
		'#type' => 'textfield', //you can find a list of available types in the form api
		'#title' => 'Логин или Email',
		'#size' => 25,
		'#maxlength' => 50,
		'#required' => TRUE, //make this field required 
	  );
	$form['password'] = array(
		'#type' => 'password', //you can find a list of available types in the form api
		'#title' => 'Пароль',
		'#size' => 25,
		'#maxlength' => 30,
		'#required' => TRUE, //make this field required 
	  );
	$form['submit_button'] = array(
		'#type' => 'submit',
		'#value' => t('Войти'),
	  );
	return $form;
}

function authorization_form_validate($form, &$form_state) 
{
	global $user;
	if($user->uid == 0)
	{
		form_set_error('login_or_email','Вы забыли войти в аккаунт на сайте. <a href="'.url('user',array('absolute'=>true)).'" >Вход на сайт здесь</a>');
	}
}

function authorization_form_submit($form, &$form_state) 
{
	global $user;
	$link = get_db_connection();
	$hash = get_password_hash($form_state['values']['password']);
	//выберем уникальный ключ пользователя по введённому логину\почте и паролю
	$query ="SELECT uniclust_users.key, uniclust_users.id_drupal_entities FROM uniclust_users WHERE (uniclust_users.login = '".$form_state['values']['login_or_email']."' OR uniclust_users.email = '".$form_state['values']['login_or_email']."') AND uniclust_users.password = '".$hash."'";
	$result = mysqli_query($link, $query) or die("Ошибка выполнения запроса" . mysqli_error($link)); 
	if($result)
	{
		$row = mysqli_fetch_array($result);
		$key_uniclust = $row['key'];
		$user_drupal_entity_id = $row['id_drupal_entities'];//какой сущности друпала принадлежит этот пользователь? потом будем сравнивать!
		$row_cnt = mysqli_num_rows($result);
		//Учётка UNICLUST с таким логином\email'ом и паролем отсутствует в базе данных UNICLUST, либо таких учёток много
		if($row_cnt != 1)
		{
			form_set_error('login_or_email','Данные введены неверно! Повторите попытку.');
			return;
		}
		//Данные верны и такая учётка UNICLUST правда существует
		else
		{
			$nodes = db_select('uniclust_drupal_user_bindings', 'DB')
			->fields('DB',array('drupal_uid'))
			->condition('DB.uniclust_key', $key_uniclust)
			->execute();
			$row_cnt = $nodes->rowCount();
			//Если этот аккаунт UNICLUST уже привязан к какому-то аккаунту Drupal
			if($row_cnt == 1)
			{
				//Если айдишники совпали, то всё огонь
				if($user->uid == $nodes->fetchAssoc()['drupal_uid'])
				{
					//ВСЁ ВЕРНО! Осталось сравнить ключи сущностей друпала, которому принадлежит данный пользователь и сущности друпала, из под которой этот пользователь пытается сейчас войти в аккаунт
					//вытягиваем уникальный ключ из этой сущности друпала
					$nodes = db_select('drupal_key_for_uniclust', 'DB')
					->fields('DB',array('unique_key'))
					->execute();
					if($nodes->rowCount()!=1)
					{
						form_set_error('login_or_email','Данная сущность Drupal не содержит уникального ключа для идентификации в UNICLUST. Если проблема повторяется - обратитесь к администратору данной сущности Drupal.');
						return;
					}
					$unique_key_of_current_drupal_entity = $nodes->fetchAssoc()['unique_key'];
					//Вытянем из БД Юникласта ключ сущности друпала, которой принадлежит данный пользователь и сравним этот ключ с ключом, который выше
					$link = get_db_connection();
					$query = "SELECT * FROM drupal_entities WHERE (drupal_entities.key = '".$unique_key_of_current_drupal_entity."' AND drupal_entities.drupal_entities_id = ".$user_drupal_entity_id." )";
					$result = mysqli_query($link, $query) or die("Ошибка выполнения запроса " . mysqli_error($link)); 
					$rowCount = mysqli_num_rows($result);
					mysqli_close($link);
					if($result && $rowCount == 1)
					{
						//ВСЁ ВЕРНО: логин\эмейл и пароль - правильные, ключ сопоставления пользователей между друпалом и юникластом - правильные, уникальный ключ сущности друпала - правильный
						return;
					}
					else
					{
						form_set_error('login_or_email','Извините, но данная учётная запись принадлежит другой сущности Drupal. Вы не можете в неё войти отсюда.');
						return;
					}
				}
				//если айдишники не совпали, то пользователь Drupal ввёл данные от чужой записи UNICLUST
				else
				{
					form_set_error('login_or_email','Данная учётная запись уже привязана к другому аккаунту Drupal.');
					return;
				}
			}
			//Если этот аккаунт UNICLUST ещё не привязан ни к какой учётке Drupal
			else
			{
				//Проверим, привязан ли данный аккаунт Drupal  к какой-то учётке UNICLUST
				$nodes = db_select('uniclust_drupal_user_bindings', 'DB')
				 ->fields('DB')
				 ->condition('DB.drupal_uid', $user->uid)
				 ->execute();
				$row_cnt = $nodes->rowCount();
				//Этот акк Drupal не привязан ни к какому аккаунту UNICLUST
				if($row_cnt!=1)
				{
					//Теперь проверим, эта учётка вообще из этой сущности друпала, или из другой?
					$key = CheckDrupalEntityKey();
					if(!$key)
					{
						form_set_error('login', 'В вашей сущности Drupal используется неккоректный ключ. Введите корректный ключ в настройках модуля UNICLUST и повторите попытку.');
						return;
					}
					
					//Вытянем из БД Юникласта ключ сущности друпала, которой принадлежит данный пользователь и сравним этот ключ с ключом, который выше
					$link = get_db_connection();
					$query = "SELECT * FROM drupal_entities WHERE (drupal_entities.key = '".$key."' AND drupal_entities.drupal_entities_id = ".$user_drupal_entity_id." )";
					$result = mysqli_query($link, $query);// or die("Ошибка выполнения запроса " . mysqli_error($link)); 
					$rowCount = mysqli_num_rows($result);
					mysqli_close($link);
					if($result && $rowCount == 1)
					{
						//ВСЁ ВЕРНО: логин\эмейл и пароль - правильные, ключ сопоставления пользователей между друпалом и юникластом - его нет вовсе,т.к. этот аккаунт юникласт пока свободен, уникальный ключ сущности друпала - правильный
						db_insert('uniclust_drupal_user_bindings')
						  ->fields(array( 
							'drupal_uid' => $user->uid,
							'uniclust_key' => $key_uniclust,
						  ))
						  ->execute();
						return;
					}
					else
					{
						form_set_error('login_or_email','Извините, но данная учётная запись принадлежит другой сущности Drupal. Вы не можете в неё войти из данной сущности Drupal.');
						return;
					}
				}
				//Этот аккаунт Drupal привязан к какому-то аккаунту UNICLUST
				else
				{
					form_set_error('login_or_email','Ваш аккаунт Drupal уже привязан к другой учётной записи Uniclust.');
					return;
				}
			}
		}
	}
}