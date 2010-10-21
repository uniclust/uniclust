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
class ClaimAdmin extends Claim
{

	// регистрация новой организации
	const TYPE_NEW_ORG = 'new_org';
	
	/**
	 * Returns the static model of the specified AR class.
	 * @return Claim the static model class
	 */
	public static function model($className=__CLASS__)
	{
		return parent::model($className);
	}

	

	/**
	 * @return array customized attribute labels (name=>label)
	 */
	public function attributeLabels()
	{
		return array(
			'id' => 'ID',
			'date' => 'Date',
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

	public function beforeValidate()
	{
		$this->type = Claim::TYPE_ADMIN;
		return parent::beforeValidate();
	}

	public function beforeSave()
	{
		$this->type = Claim::TYPE_ADMIN;
		return parent::beforeSave();
	}
}
