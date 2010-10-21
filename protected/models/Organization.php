<?php

/**
 * This is the model class for table "organizations".
 *
 * The followings are the available columns in table 'organizations':
 * @property string $id
 * @property string $russian_short_name
 * @property string $english_short_name
 * @property string $full_name
 * @property string $url
 * @property string $organization_description
 * @property string $phone
 * @property string $address
 * @property string $head
 * @property string $status
 */
class Organization extends CActiveRecord
{

	public static $statuses = array(
		'new' => 'Новая',
		'registered' => 'Зарегистрирована',
		'locked' => 'Заблокирована'
	);
	
	/**
	 * Returns the static model of the specified AR class.
	 * @return Organization the static model class
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
		return 'organizations';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('russian_short_name, english_short_name, full_name, address, head', 'required'),
			array('russian_short_name, english_short_name', 'length', 'max'=>30),
			array('full_name', 'length', 'max'=>200),
			array('url', 'length', 'max'=>250),
			array('phone', 'length', 'max'=>100),
			array('status', 'length', 'max'=>10),
			array('organization_description', 'safe'),
			// The following rule is used by search().
			// Please remove those attributes that should not be searched.
			array('id, russian_short_name, english_short_name, full_name, url, organization_description, phone, address, head, status', 'safe', 'on'=>'search'),
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
			'russian_short_name' => 'Краткое название по-русски',
			'english_short_name' => 'Краткое название латиницей',
			'full_name' => 'Полное название',
			'url' => 'Сайт',
			'organization_description' => 'Описание',
			'phone' => 'Телефоны',
			'address' => 'Адрес',
			'head' => 'ФИО главы',
			'status' => 'Статус'
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
		$criteria->compare('russian_short_name',$this->russian_short_name,true);
		$criteria->compare('english_short_name',$this->english_short_name,true);
		$criteria->compare('full_name',$this->full_name,true);
		$criteria->compare('url',$this->url,true);
		$criteria->compare('organization_description',$this->organization_description,true);
		$criteria->compare('phone',$this->phone,true);
		$criteria->compare('address',$this->address,true);
		$criteria->compare('head',$this->head,true);
		$criteria->compare('status',$this->status,true);

		return new CActiveDataProvider(get_class($this), array(
			'criteria'=>$criteria,
		));
	}

	public function beforeValidate()
	{
		if ($this->isNewRecord)
		{
			if (empty($this->status))
			{
				$this->status = 'new';
			}
		}
		return parent::beforeValidate();
	}
}
