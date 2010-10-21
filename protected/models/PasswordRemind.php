<?php

/**
 * This is the model class for table "password_reminds".
 *
 * The followings are the available columns in table 'password_reminds':
 * @property string $user_id
 * @property string $register
 * @property string $hash
 */
class PasswordRemind extends CActiveRecord
{
	/**
	 * Returns the static model of the specified AR class.
	 * @return PasswordRemind the static model class
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
		return 'password_reminds';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('user_id, hash', 'required'),
			array('user_id', 'length', 'max'=>10),
			array('register', 'length', 'max'=>3),
			array('hash', 'length', 'max'=>32),
			// The following rule is used by search().
			// Please remove those attributes that should not be searched.
			array('user_id, register, hash', 'safe', 'on'=>'search'),
		);
	}

	/**
	 * @return array relational rules.
	 */
	public function relations()
	{
		return array(
			'user' => array(self::BELONGS_TO, 'User', 'user_id')
		);
	}

	/**
	 * @return array customized attribute labels (name=>label)
	 */
	public function attributeLabels()
	{
		return array(
			'user_id' => 'User',
			'register' => 'Register',
			'hash' => 'Hash',
		);
	}

	/**
	 * Retrieves a list of models based on the current search/filter conditions.
	 * @return CActiveDataProvider the data provider that can return the models based on the search/filter conditions.
	 */
	public function search()
	{
		$criteria=new CDbCriteria;
		$criteria->compare('user_id',$this->user_id,true);
		$criteria->compare('register',$this->register,true);
		$criteria->compare('hash',$this->hash,true);

		return new CActiveDataProvider(get_class($this), array(
			'criteria'=>$criteria,
		));
	}

	public function beforeValidate()
	{			
		if (empty($this->hash))
		{
			$alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
			$size = 32;
			for (; $size > 0; --$size)
			{
				$this->hash .= $alpha[mt_rand(0, strlen($alpha)-1)];
			}
		}	
		return parent::beforeValidate();
	}
}
