<?php
/**
 * Uniclust config form.
 */
function uniclust_config_form() {
  $form = array();
  
  $form['current_drupal_entity_unique_key'] = array(
    '#type' => 'textfield',
    '#title' => t('Уникальный ключ этой сущности Drupal'),
    '#required' => TRUE,
  );
  $form['mail_admin_of_group'] = array(
    '#type' => 'textfield',
    '#title' => t('Электронный адресс'),
	'#description' => t('Если вы собираетесь ввести не использованный ранее ключ - введите незанятый для UNICLUST\'а e-mail адресс. Новый аккаунт администратора группы будет привязан к этому почтовому ящику. Если вы хотите ввести ранее использованный ключ - оставьте это поле пустым!'),
  );
 
  return system_settings_form($form);
}

function uniclust_config_form_validate($form, &$form_state)
{
	$link = get_db_connection();
	$query ="CALL `isThereSuchKeyOfDrupalEntity`('".$form_state['values']['current_drupal_entity_unique_key']."')";
	$result = mysqli_query($link, $query) or die("Ошибка выполнения запроса" . mysqli_error($link));
	if(!$result || mysqli_fetch_array($result)['Answer']=='NO')
	{
		form_set_error('current_drupal_entity_unique_key', 'Не существует сущности Drupal с таким ключом! Используйте другой ключ!');
		mysqli_close($link);
	}
	else
	{
		$row = mysqli_fetch_array($result);
		$num_deleted = db_delete('drupal_key_for_uniclust')
		  ->execute();
		 db_insert('drupal_key_for_uniclust')
		  ->fields(array( 
		  'unique_key' => $form_state['values']['current_drupal_entity_unique_key'],
		  ))
		->execute();
		//Ключ ещё не использовался никогда
		if(!$row['Using'])
		{
			//Создадим админ-аккаунт
			$link = get_db_connection();
			$query ="call `test_7`('".$form_state['values']['mail_admin_of_group']."', 1, 1, '', '".$form_state['values']['current_drupal_entity_unique_key']."')";
			$result = mysqli_query($link, $query);// or die("Ошибка выполнения запроса" . mysqli_error($link));
			//проверим, создалась ли новая учётка администратору группы
			if(mysqli_error($link) == "Duplicate entry '".$form_state['values']['mail_admin_of_group']."' for key 'email'")
			{
				form_set_error('mail_admin_of_group', 'Данный почтовый ящик уже занят каким-то аккаунтом UNICLUST. Используйте свободный почтовый ящик!');
				mysqli_close($link);
				return;
			}
			else if(mysqli_error($link) != NULL)
			{
				form_set_error('mail_admin_of_group', 'Возникла непредвиденная ошибка при создании новой учётной записи администратора группы для данного ключа. Повторите ошибку позже.');
				mysqli_close($link);
				return;
			}
			else
			{
				//Учётка создана, всё гуд!!! Теперь нужно ключ пометить как используемый!
				$new_usr = mysqli_fetch_array($result);
				mysqli_close($link);
				$link = get_db_connection();
				$query ="call `SetKeyToUsing`('".$form_state['values']['current_drupal_entity_unique_key']."')";
				$result = mysqli_query($link, $query);// or die("Ошибка выполнения запроса" . mysqli_error($link));
				if($result && mysqli_affected_rows($link))
				{
					drupal_mail('system', 'mail', $form_state['values']['mail_admin_of_group'], language_default(), array(
					  'context' => array(
					  'subject' => 'Создан админ-аккаунт UNICLUST',
					  'message' => 'Здравствуйте! Вы развернули Drupal-сайт, установили модуль UNICLUST, и указали правильный ключ сущности Drupal. В системе UNICLUST был создан админ-аккаунт с данным почтовым ящиком. Логин: '.$new_usr['login'].' Пароль: '.$new_usr['password'].' Пароль вы можете изменить в личном кабинете UNICLUST на Вашем сайте. С уважением администрация UNICLUST!',
					  )
					));
					drupal_set_message("Ваш админ-аккаунт для модуля UNICLUST был создан.<br/>Письмо с данными аккаунта было отправлено на указанный почтовый ящик.<br /> Логин:".$new_usr['login']."<br />Пароль:".$new_usr['password']."<br />E-mail:".$new_usr['email']);
					mysqli_close($link);
				}
				else
				{
					form_set_error('current_drupal_entity_unique_key', 'Админ аккаунт был создан, но, к сожалению, не удалось установить данный ключ как используемый. Обратитесь к администратору Uniclust, чтобы он пометил данный ключ как используемый в поле "using" в соответствующей таблице базы данных Uniclust.');
					mysqli_close($link);
				}
			}
		}
		else
		{
			drupal_set_message("Введённый ключ сущности Drupal уже был использован. Вы должны знать данные для входа в UNICLUST под сущностью, которая использовала этот ключ.");
		}
	}
	return;
}

function uniclust_config_form_submit($form, &$form_state)
{
	return;
}