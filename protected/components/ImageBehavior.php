<?php

class ImageBehavior extends CActiveRecordBehavior {

    public $instance = null;
    public $savePath = null;
    public $idField = 'id';
    public $resize = true;
    public $resizeHeight = 100;
    public $resizeWidth = 100;
    public $imageFormat = 'png';

    public function afterSave($event)
    {
		if ($this->instance)
		{
			if (is_null($this->savePath))
			{
				throw new Exception("null savePath given");
			}
			if (is_null($this->idField))
			{
				throw new Exception("null filename given");
			}
			$savePath = $this->savePath.$this->Owner->{$this->idField}.'.'.$this->imageFormat;
			//dirname(Yii::app()->getBasePath()).'/'.Yii::app()->params['pflnewspicPath'].$model->id.'.png';
			$imgObject = Yii::app()->image->load($this->instance->getTempName());
			$imgObject->resize($this->resizeWidth, $this->resizeHeight, Image::AUTO);
			return $imgObject->save($savePath);
		} else {
			return true;
		}
	}

}
