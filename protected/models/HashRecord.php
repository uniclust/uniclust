<?php

/**
 * This is the model class for table "hash".
 *
 * The followings are the available columns in table 'hash':
 * @property string $user_name
 * @property string $login
 * @property string $email
 * @property string $date_label
 * @property string $hash
 */
class HashRecord extends CActiveRecord
{
	/**
	 * Returns the static model of the specified AR class.
	 * @return HashRecord the static model class
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
		return 'hash';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('user_name, login, email, date_label', 'required'),
			array('user_name, email', 'length', 'max'=>100),
			array('login', 'length', 'max'=>20),
			array('hash', 'safe'),
			// The following rule is used by search().
			// Please remove those attributes that should not be searched.
			array('user_name, login, email, date_label, hash', 'safe', 'on'=>'search'),
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
			'user_name' => 'User Name',
			'login' => 'Login',
			'email' => 'Email',
			'date_label' => 'Date Label',
			'hash' => 'Hash',
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

		$criteria->compare('user_name',$this->user_name,true);
		$criteria->compare('login',$this->login,true);
		$criteria->compare('email',$this->email,true);
		$criteria->compare('date_label',$this->date_label,true);
		$criteria->compare('hash',$this->hash,true);

		return new CActiveDataProvider(get_class($this), array(
			'criteria'=>$criteria,
		));
	}
}