<?php

class WebUser extends CWebUser {
    private $_model = null;
 /*
    function getStatus()
    {
        return $this->getModel()->status;
    }

    function getGender()
    {
		return $this->getModel()->gender;
	}

	
    function getName()
    {
		return $this->getModel()->name;
	}
	*/
	function isAdmin()
	{
		return $this->login == Yii::app()->params['adminLogin'];
	}
    
	function getLogin()
	{
		return $this->getModel()->login;
	}
 
    public function getModel(){
		/* if ($this->isGuest)
		{
			throw new Exception("Not logged in", 0);
		} */
        if (!$this->isGuest && $this->_model === null){
            $this->_model = User::model()->findByPk($this->id, array('select' => 'login, full_user_name'));
        }
        return $this->_model;
    }
}
