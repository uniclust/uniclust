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
	public $primaryOrganization;
	

	

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('login, full_user_name, latin_user_name, primary_email, primaryOrganization', 'required'),
			array('login', 'length', 'max'=>20),
			array('full_user_name, latin_user_name, phones, primary_email', 'length', 'max'=>250),
			array('user_status, date_of_registration', 'length', 'max'=>10),
		);
	}

	

	/**
	 * @return array customized attribute labels (name=>label)
	 */
	public function attributeLabels()
	{
		return array(
			'login' => 'Логин',
			'full_user_name' => 'Полное имя',
			'latin_user_name' => 'Полное имя латиницей',
			'primary_email' => 'Основной e-mail',
			'primaryOrganization' => 'Основная организация'
		);
	}
	

}
