<?php

/**
 * This is the model class for table "user_organization_relations".
 *
 * The followings are the available columns in table 'user_organization_relations':
 * @property string $user_id
 * @property string $organization_id
 * @property string $is_primary
 * @property string $organization_position
 * @property string $status
 */
class UserOrganizationRelation extends CActiveRecord
{
	public static $statusNames = array(
		'new' => 'Ожидание подтверждения',
		'registered' => 'Участник',
		'head' => 'Глава',
	);

	public static $statusHelps = array(
		'new' => 'Ваше участие в группе еще не подтверждено',
		'registered' => 'Вы участник этой группы',
		'head' => 'Вы глава этой группы'
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
		return 'user_organization_relations';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('user_id, organization_id, status', 'length', 'max'=>10),
			array('is_primary', 'length', 'max'=>3),
			array('position', 'length', 'max'=>100),
			// The following rule is used by search().
			// Please remove those attributes that should not be searched.
			array('user_id, organization_id, is_primary, position, status', 'safe', 'on'=>'search'),
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
			'organization' => array(self::BELONGS_TO, 'Organization', 'organization_id')
		);
	}

	/**
	 * @return array customized attribute labels (name=>label)
	 */
	public function attributeLabels()
	{
		return array(
			'user_id' => 'User',
			'organization_id' => 'Organization',
			'is_primary' => 'Is Primary',
			'position' => 'Organization Position',
			'status' => 'Status',
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
		$criteria->compare('organization_id',$this->organization_id,true);
		$criteria->compare('is_primary',$this->is_primary,true);
		$criteria->compare('position',$this->organization_position,true);
		$criteria->compare('status',$this->status,true);

		return new CActiveDataProvider(get_class($this), array(
			'criteria'=>$criteria,
		));
	}
}
