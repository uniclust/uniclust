<?php

/**
 * This is the model class for table "user_multiprocessor_relations".
 *
 * The followings are the available columns in table 'user_multiprocessor_relations':
 * @property string $user_id
 * @property string $multiprocessor_id
 * @property string $primary_group
 * @property string $user_status
 * @property string $login_on_machine
 * @property string $uid_on_machine
 * @property string $registration_date
 * @property string $request_tpl
 */
class UserMultiprocessorRelation extends CActiveRecord
{
	public static $statusNames = array(

	);

	public static $statusHelps = array(

	);
	
	public static function model($className=__CLASS__)
	{
		return parent::model($className);
	}

	/**
	 * @return string the associated database table name
	 */
	public function tableName()
	{
		return 'user_multiprocessor_relations';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('user_id, multiprocessor_id, login_on_machine, request_tpl', 'required'),
			array('user_id, multiprocessor_id, primary_group, user_status, uid_on_machine', 'length', 'max'=>10),
			array('login_on_machine', 'length', 'max'=>20),
			array('registration_date', 'safe'),
			// The following rule is used by search().
			// Please remove those attributes that should not be searched.
			array('user_id, multiprocessor_id, primary_group, user_status, login_on_machine, uid_on_machine, registration_date, request_tpl', 'safe', 'on'=>'search'),
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
			'user_id' => 'User',
			'multiprocessor_id' => 'Multiprocessor',
			'primary_group' => 'Primary Group',
			'user_status' => 'User Status',
			'login_on_machine' => 'Login On Machine',
			'uid_on_machine' => 'Uid On Machine',
			'registration_date' => 'Registration Date',
			'request_tpl' => 'Request Tpl',
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

		$criteria->compare('user_id',$this->user_id,true);
		$criteria->compare('multiprocessor_id',$this->multiprocessor_id,true);
		$criteria->compare('primary_group',$this->primary_group,true);
		$criteria->compare('user_status',$this->user_status,true);
		$criteria->compare('login_on_machine',$this->login_on_machine,true);
		$criteria->compare('uid_on_machine',$this->uid_on_machine,true);
		$criteria->compare('registration_date',$this->registration_date,true);
		$criteria->compare('request_tpl',$this->request_tpl,true);

		return new CActiveDataProvider(get_class($this), array(
			'criteria'=>$criteria,
		));
	}
}
