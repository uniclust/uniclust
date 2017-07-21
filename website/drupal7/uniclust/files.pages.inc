<?php
function files_uniclust_callback(&$form = NULL, &$form_state = NULL) 
{
	$current_user = getFullUniclustUserInfo();
	if($current_user['id'] == 0) drupal_access_denied();//drupal_not_found();
	$page['static_content'] = array('#markup'=>'<p>Здравствуйте! На этой странице Вы можете загружать новые файлы и просматривать список загруженных ранее файлов.</p>');
	
	
	$page['upload_form'] = drupal_get_form('upload_file_form');
	$path = file_stream_wrapper_get_instance_by_uri('public://')->realpath().'\\uniclust_files\\'.$current_user['id'];
	$page['list_of_files'] = array('#markup'=>generateListOfFilesHTMLCode($path, $current_user['id']));
	//$page['list_of_files'] = array('#markup'=>getcwd());
	//$page['list_of_files'] = array('#markup'=> file_stream_wrapper_get_instance_by_uri('public://')->realpath().'\\uniclust_files\\'.$current_user['id']);
	return $page;
}

function upload_file_form() {
  $form['file'] = array(
    '#type' => 'file',
    '#title' => 'Файл',
    '#description' => 'Выберите файл для загрузки',
	//'#required' => TRUE
  );
 
  $form['submit'] = array(
    '#type' => 'submit',
    '#value' => 'Загрузить',
  );
 
  return $form;
}
 

function upload_file_form_validate($form, &$form_state) 
{
	$validators = array(
		//'file_validate_is_image' => array(), // Проверка, действительно ли файл является изображением
		//'file_validate_extensions' => array('png gif jpg jpeg'), // Проверка на расширения
		'file_validate_size' => array(512 * 1024 * 1024), // Проверка на размер файла (максимум 512mb)
	);  
	if ($wrapper = file_stream_wrapper_get_instance_by_uri('public://')) 
	{
		$realpath = $wrapper->realpath();
		$current_user = getFullUniclustUserInfo();
		if(!is_dir($realpath.'\\uniclust_files\\'.$current_user['id']))
		{
			if(!mkdir($realpath.'\\uniclust_files\\'.$current_user['id']))
			{
				form_set_error('Не удалось создать папку для закачки файлов.');
				return;
			}
		}
		if ($file = file_save_upload('file', $validators, 'public://uniclust_files/'.$current_user['id'])) 
		{
			$form_state['values']['file'] = $file; // передаём информацию о файле в ф-ю uniclust_form_submit()
			$form_state['values']['uniclust_user_id'] = $current_user['id'];
		}
		else 
		{
			form_set_error('file', 'Файл не был загружен');
		}
	}
	else
	{
		form_set_error('file', 'Не удалось получить путь для сохранения файла. Обратитесь к');
	}
}
 

function upload_file_form_submit($form, &$form_state) {
	$file = $form_state['values']['file'];
	$uniclust_user_id = $form_state['values']['uniclust_user_id'];
	
	$file->status = FILE_STATUS_PERMANENT; // Изменяем статус файла на "Постоянный"
	$run = file_save($file); // Сохраняем новый статус
	$parts_of_path = explode('/', $run->destination);
	$new_filename = array_pop($parts_of_path);
	$full_path_to_file = file_stream_wrapper_get_instance_by_uri('public://')->realpath().'\\uniclust_files\\'.$uniclust_user_id.'\\'.$new_filename;
	$full_path_to_file_for_sql = str_replace('\\','\\\\', $full_path_to_file);
	
	
	//заносим в БД Юникласта файл
	$link = get_db_connection();
	$query = "INSERT INTO `uniclust_files` (`name`, `status`, `user_id`, `size`, `full_path`) VALUES('".$file->filename."', 'ready', ".$uniclust_user_id.", ".$file->filesize.", '".$full_path_to_file_for_sql."')";
	$result = mysqli_query($link, $query);
	mysqli_close($link);
	if($result)
	{
		drupal_set_message('Файл загружен! Имя файла: '.$new_filename.'. Полный путь к файлу:'.$full_path_to_file);
		return;
	}
	form_set_error('file','Не удалось загрузить файл. Ошибка подключения к базе данных Uniclust.');
	
}

function generateListOfFilesHTMLCode($path, $uniclust_user_id)
{
	$code = '<p>Список Ваших файлов:</p><ul>';
	/*if(is_dir($path))
	{
		$files = scandir($path);

		for($i=2;$i<count($files);$i++)
		{
			$code .= '<li>'.$files[$i].'</li>';
		}
	}*/
	
	
	
	$link = get_db_connection();
	$query = "SELECT * FROM `uniclust_files` WHERE `uniclust_files`.user_id = ".$uniclust_user_id;
	$result = mysqli_query($link, $query);
	mysqli_close($link);
	if($result)
	{
		while($row = mysqli_fetch_array($result))
		{
			$code .= '<li>'.$row['name'].'</li>';
		}
	}
	
	
	$code .= '</ul>';
	return $code;
}