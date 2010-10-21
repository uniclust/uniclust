<?php

/**
 * This is the model class for table "group_multiprocessor_relations".
 *
 * The followings are the available columns in table 'group_multiprocessor_relations':
 * @property string $group_id
 * @property string $multiprocessor_id
 * @property string $status
 * @property integer $curator_id
 * @property string $request_tpl
 */
class GroupMultiprocessorRelation extends CActiveRecord
{
	/**
	 * Returns the static model of the specified AR class.
	 * @return GroupMultiprocessorRelation the static model class
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
		return 'group_multiprocessor_relations';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('group_id, multiprocessor_id', 'required'),
			array('curator_id', 'numerical', 'integerOnly'=>true),
			array('group_id, multiprocessor_id', 'length', 'max'=>10),
			array('status', 'length', 'max'=>11),
			array('request_tpl', 'safe'),
			// The following rule is used by search().
			// Please remove those attributes that should not be searched.
			array('group_id, multiprocessor_id, status, curator_id, request_tpl', 'safe', 'on'=>'search'),
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
			'group_id' => 'Group',
			'multiprocessor_id' => 'Multiprocessor',
			'status' => 'Status',
			'curator_id' => 'Curator',
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

		$criteria->compare('group_id',$this->group_id,true);
		$criteria->compare('multiprocessor_id',$this->multiprocessor_id,true);
		$criteria->compare('status',$this->status,true);
		$criteria->compare('curator_id',$this->curator_id);
		$criteria->compare('request_tpl',$this->request_tpl,true);

		return new CActiveDataProvider(get_class($this), array(
			'criteria'=>$criteria,
		));
	}
}