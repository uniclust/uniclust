<?php

/**
 * This is the model class for table "claims".
 *
 * The followings are the available columns in table 'claims':
 * @property string $id
 * @property string $date
 * @property string $type
 * @property string $subtype
 * @property string $user_id
 * @property string $target_id
 * @property string $is_primary
 * @property string $param1
 * @property string $param2
 * @property string $data
 * @property string $considered
 * @property string $considered_by
 * @property string $consideration_date
 * @property string $reason
 */
class Claim extends CActiveRecord
{

	const TYPE_HEAD = 'head';
	const TYPE_MP = 'mp';
	const TYPE_ADMIN = 'admin';
	const TYPE_CURATOR = 'curator';
	
	/**
	 * Returns the static model of the specified AR class.
	 * @return Claim the static model class
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
		return 'claims';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('date, type, subtype, user_id, target_id, is_primary, param1, param2, data, considered_by, consideration_date, reason', 'required'),
			array('type', 'length', 'max'=>7),
			array('subtype', 'length', 'max'=>50),
			array('user_id, target_id, considered_by', 'length', 'max'=>10),
			array('is_primary, param1, param2', 'length', 'max'=>100),
			array('considered', 'length', 'max'=>11),
			// The following rule is used by search().
			// Please remove those attributes that should not be searched.
			array('id, date, type, subtype, user_id, target_id, is_primary, param1, param2, data, considered, considered_by, consideration_date, reason', 'safe', 'on'=>'search'),
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
			'date' => 'Date',
			'type' => 'Type',
			'subtype' => 'Subtype',
			'user_id' => 'User',
			'target_id' => 'Target',
			'is_primary' => 'Is Primary',
			'param1' => 'Param1',
			'param2' => 'Param2',
			'data' => 'Data',
			'considered' => 'Considered',
			'considered_by' => 'Considered By',
			'consideration_date' => 'Consideration Date',
			'reason' => 'Reason',
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
		$criteria->compare('date',$this->date,true);
		$criteria->compare('type',$this->type,true);
		$criteria->compare('subtype',$this->subtype,true);
		$criteria->compare('user_id',$this->user_id,true);
		$criteria->compare('target_id',$this->target_id,true);
		$criteria->compare('is_primary',$this->is_primary,true);
		$criteria->compare('param1',$this->param1,true);
		$criteria->compare('param2',$this->param2,true);
		$criteria->compare('data',$this->data,true);
		$criteria->compare('considered',$this->considered,true);
		$criteria->compare('considered_by',$this->considered_by,true);
		$criteria->compare('consideration_date',$this->consideration_date,true);
		$criteria->compare('reason',$this->reason,true);

		return new CActiveDataProvider(get_class($this), array(
			'criteria'=>$criteria,
		));
	}
}
