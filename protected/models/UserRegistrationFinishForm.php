<?php

/**
 * Форма ввода дополнительной информации для завершения регистрации
 *
 * @property string $password
 * @property string $password2
 * @property string $organizationPosition
 * @property string $phones
 * @property string $interests
 * @property string $otherInformation
 */
class UserRegistrationFinishForm extends CFormModel
{
	public $password,
		   $password2,
		   $organizationPosition,
		   $phones,
		   $interests,
		   $otherInformation;		

	public function rules()
	{
		return array(
			array('password, password2, organizationPosition', 'required'),
			array('phones, interests, otherInformation', 'length', 'max'=>2000),
			array('password', 'compare', 'compareAttribute'=>'password2')
		);
	}

	public function attributeLabels()
	{
		return array(
			'password' => 'Пароль',
		    'password2' => 'Пароль еще раз',
		    'organizationPosition' => 'Должность в организации',
		    'phones' => 'Контактные телефоны',
		    'interests' => 'Интересы',
		    'otherInformation' => 'Другая информация'
		);
	}

}
