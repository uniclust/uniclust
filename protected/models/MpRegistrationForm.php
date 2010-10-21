<?php

/**
 * This is the model class for table "users".
 *
 * The followings are the available columns in table 'users':
 * @property string $id
 * @property string $login
 * @property string $password
 * @property string $full_user_name
 * @property string $latin_user_name
 * @property string $phones
 * @property string $interests
 * @property string $other_information
 * @property string $user_status
 * @property string $date_of_registration
 * @property string $primary_email
 */
class UserRegistrationForm extends User
{
	public $orgId,
		   $name,
		   $login,
		   $url,
		   $supportEmail,
		   $publicAccess,
		   $dnsAddressesList,
		   $description; 

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('orgId, name, login, supportEmail, $publicAccess', 'required'),
			array('dnsAddressesList, url, description', 'safe')
		);
	}

	

	/**
	 * @return array customized attribute labels (name=>label)
	 */
	public function attributeLabels()
	{
		return array(
			'orgId' => 'Организация, в которой расположена машина',
		    'name' => 'Имя машины',
		    'login'  => 'Ваш логин на машине',
		    'url' => 'Ссылка на сайт машины',
		    'supportEmail' => 'Адрес тех. поддержки',
		    'publicAccess' => 'Доступна для членов других организаций',
		    'dnsAddressesList' => 'Список DNS адресов, с которых доступна машина',
		    'description' => 'Описание характеристик машины'
		);
	}
	

}
