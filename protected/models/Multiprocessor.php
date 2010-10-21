<?php

/**
 * This is the model class for table "multiprocessors".
 *
 * The followings are the available columns in table 'multiprocessors':
 * @property string $id
 * @property string $name
 * @property string $organization_id
 * @property string $public_access
 * @property string $url
 * @property string $support_email
 * @property string $dns_addresses_list
 * @property string $description
 * @property string $status
 * @property string $access_key
 */
class Multiprocessor extends CActiveRecord
{
	/**
	 * Returns the static model of the specified AR class.
	 * @return Multiprocessor the static model class
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
		return 'multiprocessors';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('name, organization_id, public_access, support_email, description', 'required'),
			array('name', 'length', 'max'=>20),
			array('organization_id, status', 'length', 'max'=>10),
			array('public_access', 'length', 'max'=>3),
			array('url, dns_addresses_list', 'length', 'max'=>250),
			array('support_email', 'length', 'max'=>100),
			array('access_key', 'length', 'max'=>32),
			// The following rule is used by search().
			// Please remove those attributes that should not be searched.
			array('id, name, organization_id, public_access, url, support_email, dns_addresses_list, description, status, access_key', 'safe', 'on'=>'search'),
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
			'name' => 'Name',
			'organization_id' => 'Organization',
			'public_access' => 'Public Access',
			'url' => 'Url',
			'support_email' => 'Support Email',
			'dns_addresses_list' => 'Dns Addresses List',
			'description' => 'Description',
			'status' => 'Status',
			'access_key' => 'Access Key',
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
		$criteria->compare('name',$this->name,true);
		$criteria->compare('organization_id',$this->organization_id,true);
		$criteria->compare('public_access',$this->public_access,true);
		$criteria->compare('url',$this->url,true);
		$criteria->compare('support_email',$this->support_email,true);
		$criteria->compare('dns_addresses_list',$this->dns_addresses_list,true);
		$criteria->compare('description',$this->description,true);
		$criteria->compare('status',$this->status,true);
		$criteria->compare('access_key',$this->access_key,true);

		return new CActiveDataProvider(get_class($this), array(
			'criteria'=>$criteria,
		));
	}
}