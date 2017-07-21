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
	//Выберем ключ пользователя Uniclust и айди сущности Друпала по введённым данным в поля(логин\мыло и пароль)
	//1. Если такого нет, то данные введены неверно!
	//2. Если такой есть: Сравниваем ключ привязки: выбираем айди пользователя Друпал из таблицы привязок аккаунтов с ключом, который мы получили из найденного аккаунта Uniclust
	//2.1. Такого айди нет, следовательно введённый аакаунт Uniclust не привязан ни к одной учётке данной сущности Друпала. Посмотрим, возможно этот аккаунт Друпал привязан к другому аккаунту Uniclust (делаем выборку из таблицы привязки аккаунтов по айди текущего пользователя Друпал)
	//2.2. Такой айди есть(см. пункт 2.2. ниже)
	//2.1.1 Текущий аккаунт Друпал уже привязан к какой учётной записи Uniclust и, по-идее, при таких обстоятельствах, пользователь сразу переадресовывается с данный страницы в рабочую среду Uniclust, но если этого не произошло, то мы выдаём ошибку о том, что данный аккаунт Друпал уже привязан к какой-то учётке Uniclust.
	//2.1.2 Текущий аккаунт Друпал не привязан ни к какой учётке Uniclust, проверим ключ сущности Друпала на правильность
	//2.1.2.1 Ключ сущности неверный! Выводим ошибку
	//2.1.2.2 Ключ сущности верный - проверяем, к какой сущности Друпала принадлежит введённый пользователь Uniclust(выбираем айди сущности Друпала из таблицы drupal_entities из БД Uniclust по ключу и айди сущности Друпала(который мы откопали у пользователя), который указан в конфигурациях данного модуля)
	//2.1.2.2.1 Введённый пользователь Uniclust принадлежит именно этой сущности - заносим привязку в таблицу привязок БД Друпала, всё хорошо!!!!!
	//2.1.2.2.2 Введённый пользователь Uniclust принадлежит сущности Друпал с другим ключом - выдаём ошибку
	//2.2. В таблице привязок аккаунтов есть такая запись, у которой ключ совпадает с тем, что мы выбрали из БД Uniclust. Сверим айди текущего пользователя Друпал и тот, что мы получили из таблицы привязок
	//2.2.1. Эти два айди совпадают, проверяем ключ сущности Друпала на правильность (checkDrupalEntityKey)
	//2.2.2. Эти два айди не совпадают, следовательно, под введённым аккаунтом Uniclust работает другой пользователь Друпал. Выдаём ошибку.
	//2.2.1.1 Ключ сущности Друпал указан неверно - выводим ошибку
	//2.2.1.1 Ключ сущности Друпал указан верно. Теперь проверяем, принадлежит ли введённый пользователь Uniclust именно этой сущности Drupal, или другой
	//2.2.1.1.1 Введённый пользователь Uniclust указан верно, но он принадлежит другой сущности Drupal - выводим ошибку!
	//2.2.1.1.2 Введённый пользователь Uniclust введён верно, всё хорошо!!!!!
	global $user;
	$link = get_db_connection();
	$hash = get_password_hash($form_state['values']['password']);
	//выберем уникальный ключ пользователя Юникласт из БД Юникласт по введённому логину\почте и паролю
	$query = "SELECT uniclust_users.key, uniclust_users.id_drupal_entities FROM uniclust_users WHERE (uniclust_users.login = '".$form_state['values']['login_or_email']."' OR uniclust_users.email = '".$form_state['values']['login_or_email']."') AND uniclust_users.password = '".$hash."'";
	$result = mysqli_query($link, $query);// or die("Ошибка выполнения запроса" . mysqli_error($link)); 
	if($result)
	{
		
		$row_cnt = mysqli_num_rows($result);
		//учётка UNICLUST с таким логином\email'ом и паролем отсутствует в базе данных UNICLUST, либо таких учёток много (чего быть не может).
		if($row_cnt != 1)
		{
			form_set_error('login_or_email','Данные введены неверно! Повторите попытку.');
			return;
		}
		//Данные введены верно и такая учётка UNICLUST правда существует
		else
		{
			$row = mysqli_fetch_array($result);
			$key_uniclust = $row['key'];//ключ пользователя Uniclust, от которого введены данные
			$user_drupal_entity_id = $row['id_drupal_entities'];//какой сущности друпала принадлежит этот пользователь? потом будем сравнивать!
			
			//выбираем айди пользователя Друпала из таблицы uniclust_drupal_user_bindings по ключу аккаунта Uniclust, от которого введены данные
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
					//проверяем ключ сущности Друпал на правильность
					$entity_answer = checkDrupalEntityKey();
					if($entity_answer == NULL)
					{
						form_set_error('login_or_email','Данная сущность Drupal содержит неверный ключ сущности. Если проблема повторяется - обратитесь к администратору данной сущности Drupal.');
						return;
					}
					//Теперь проверим, введённый пользователь Uniclust, принадлежит ли он именно этой сущности друпал
					if($entity_answer['id_drupal_entity'] != $user_drupal_entity_id)
					{
						form_set_error('login_or_email','Указанный пользователь Uniclust принадлежит другой сущности Drupal. Если проблема повторяется - обратитесь к администратору данной сущности Drupal.');
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
					$key = checkDrupalEntityKey();
					if(!$key)
					{
						form_set_error('login', 'В вашей сущности Drupal используется неккоректный ключ. Введите корректный ключ в настройках модуля UNICLUST и повторите попытку.');
						return;
					}
					
					//Вытянем из БД Юникласта ключ сущности друпала, которой принадлежит данный пользователь и сравним этот ключ с ключом, который выше
					$link = get_db_connection();
					$query = "SELECT * FROM drupal_entities WHERE (drupal_entities.key = '".$key['entity_key']."' AND drupal_entities.drupal_entities_id = ".$user_drupal_entity_id." )";
					$result = mysqli_query($link, $query);// or die("Ошибка выполнения запроса " . mysqli_error($link)); 
					mysqli_close($link);
					if($result && mysqli_num_rows($result) == 1)
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