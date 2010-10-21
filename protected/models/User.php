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
class User extends CActiveRecord
{
	/**
	 * Returns the static model of the specified AR class.
	 * @return User the static model class
	 */
	public static function model($className=__CLASS__)
	{
		return parent::model($className);
	}

	/**
	 * @return string the associated database table name
	 */
	public function tableName()
	{
		return 'users';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('login, password, full_user_name, latin_user_name, date_of_registration, primary_email', 'required'),
			array('login', 'length', 'max'=>20),
			array('password', 'length', 'max'=>200),
			array('full_user_name, latin_user_name, phones, primary_email', 'length', 'max'=>250),
			array('user_status, date_of_registration', 'length', 'max'=>10),
			array('interests, other_information', 'safe'),
			// The following rule is used by search().
			// Please remove those attributes that should not be searched.
			array('id, login, password, full_user_name, latin_user_name, phones, interests, other_information, user_status, date_of_registration, primary_email', 'safe', 'on'=>'search'),
		);
	}

	/**
	 * @return array relational rules.
	 */
	public function relations()
	{
		// NOTE: you may need to adjust the relation name and the related
		// class name for the relations automatically generated below.
		return array(
		);
	}

	/**
	 * @return array customized attribute labels (name=>label)
	 */
	public function attributeLabels()
	{
		return array(
			'id' => 'ID',
			'login' => 'Login',
			'password' => 'Password',
			'full_user_name' => 'Full User Name',
			'latin_user_name' => 'Latin User Name',
			'phones' => 'Phones',
			'interests' => 'Interests',
			'other_information' => 'Other Information',
			'user_status' => 'User Status',
			'date_of_registration' => 'Date Of Registration',
			'primary_email' => 'Primary Email',
		);
	}

	/**
	 * Retrieves a list of models based on the current search/filter conditions.
	 * @return CActiveDataProvider the data provider that can return the models based on the search/filter conditions.
	 */
	public function search()
	{
		// Warning: Please modify the following code to remove attributes that
		// should not be searched.

		$criteria=new CDbCriteria;

		$criteria->compare('id',$this->id,true);
		$criteria->compare('login',$this->login,true);
		$criteria->compare('password',$this->password,true);
		$criteria->compare('full_user_name',$this->full_user_name,true);
		$criteria->compare('latin_user_name',$this->latin_user_name,true);
		$criteria->compare('phones',$this->phones,true);
		$criteria->compare('interests',$this->interests,true);
		$criteria->compare('other_information',$this->other_information,true);
		$criteria->compare('user_status',$this->user_status,true);
		$criteria->compare('date_of_registration',$this->date_of_registration,true);
		$criteria->compare('primary_email',$this->primary_email,true);

		return new CActiveDataProvider(get_class($this), array(
			'criteria'=>$criteria,
		));
	}
}
