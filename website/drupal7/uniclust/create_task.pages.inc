<?php
function create_task_uniclust_callback(&$form = NULL, &$form_state = NULL) 
{
	$current_user = getFullUniclustUserInfo();
	if($current_user['id'] == 0) drupal_access_denied();//drupal_not_found();
	$page['static_content'] = array('#markup'=>'<p>Здравствуйте! На этой странице Вы можете создать новую задачу для выполнения на суперкомпьютере!</p>');
	$page['create_task_form'] = drupal_get_form('create_task_form');
	
	
	
	return $page;
}


function create_task_form()
{
	//здесь должна генерироваться форма согласно загруженному JSON-файлу
	$uniclust_user_id = getFullUniclustUserInfo()['id'];
	$user_files = array();
	$link = get_db_connection();
	$query = "SELECT * FROM `uniclust_files` WHERE `uniclust_files`.user_id = ".$uniclust_user_id;
	$result = mysqli_query($link, $query);
	mysqli_close($link);
	if($result)
	{
		$i = 0;
		while($row = mysqli_fetch_array($result))
		{
			//$code .= '<li>'.$row['name'].'</li>';
			$user_files[$i] = $row['name'];
			$i = $i+1;
		}
	}
	$form['task_name'] = array(
		'#type' => 'textfield', //you can find a list of available types in the form api
		'#title' => t('Название задачи:'),
		'#size' => 50,
		'#maxlength' => 100,
		'#required' => TRUE, //make this field required 
	  );
	$form['multiprocessor_select'] = array(
       '#type' => 'select',
       '#title' => t('Выберите суперкомпьютер:'),
       '#options' => array(0 => 'IBM Blue Gene/P ', 1 => 'IBM pSeries 690 HPC Regatta', 2 => 'Ломоносов-1', 3 => 'Ломоносов-2'),
	   '#required' => TRUE, //make this field required 
	  );
	$form['task_select'] = array(
       '#type' => 'select',
       '#title' => t('Выберите класс программы из списка для выполнения на суперкомпьютере:'),
       '#options' => array(0 => 'Matrix Processing'),
	   '#required' => TRUE, //make this field required 
	  );
	$form['action_select'] = array(
       '#type' => 'select',
       '#title' => t('Действие:'),
       '#options' => array(0 => 'Rotate',1 => 'Skew',2 => 'Scale'),
	   '#required' => TRUE, //make this field required 
	  );
	$form['angle'] = array(
		'#type' => 'textfield', //you can find a list of available types in the form api
		'#title' => t('Угол:'),
		'#size' => 5,
		'#maxlength' =>10,
		'#required' => TRUE, //make this field required 
	  );
	$form['file_select'] = array(
       '#type' => 'select',
       '#title' => t('Выберите файл для обработки:'),
       '#options' => $user_files,
	   '#required' => TRUE, //make this field required 
	  );
	$form['submit_button'] = array(
		'#type' => 'submit',
		'#value' => t('Создать задачу'),
	  );
	 
	return $form;
}
/*
function create_task_form_validate($form, &$form_state)
{
	//здесь должно проверяться соответствие аргументов согласно загруженному JSON-файлу
}

function create_task_form_submit($form, &$form_state)
{
	//здесь должен генерироваться JSON-файл с введёнными пользователями аргументами и загружаться в БД
}*/