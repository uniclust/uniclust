<?php

class ClaimController extends Controller
{
	/**
	 * @var string the default layout for the views. Defaults to '//layouts/column2', meaning
	 * using two-column layout. See 'protected/views/layouts/column2.php'.
	 */
	public $layout='//layouts/column2';

	/**
	 * @return array action filters
	 */
	public function filters()
	{
		return array(
			'accessControl', // perform access control for CRUD operations
		);
	}

	/**
	 * Specifies the access control rules.
	 * This method is used by the 'accessControl' filter.
	 * @return array access control rules
	 */
	public function accessRules()
	{
		return array(
			array('allow',  // allow all users to perform 'index' and 'view' actions
				'users'=>array('admin'),
			),
			array('allow', // allow authenticated user to perform 'create' and 'update' actions
				'actions'=>array('create','update'),
				'users'=>array('@'),
			),
			array('allow', // allow admin user to perform 'admin' and 'delete' actions
				'actions'=>array('admin','delete'),
				'users'=>array('admin'),
			),
			array('deny',  // deny all users
				'users'=>array('*'),
			),
		);
	}

	/**
	 * Displays a particular model.
	 * @param integer $id the ID of the model to be displayed
	 */
	public function actionView($id)
	{
		$this->render('view',array(
			'model'=>$this->loadModel($id),
		));
	}

	/**
	 * Creates a new model.
	 * If creation is successful, the browser will be redirected to the 'view' page.
	 */
	public function actionCreate()
	{
		$model=new Claim;

		// Uncomment the following line if AJAX validation is needed
		// $this->performAjaxValidation($model);

		if(isset($_POST['Claim']))
		{
			$model->attributes=$_POST['Claim'];
			if($model->save())
				$this->redirect(array('view','id'=>$model->id));
		}

		$this->render('create',array(
			'model'=>$model,
		));
	}

	/**
	 * Updates a particular model.
	 * If update is successful, the browser will be redirected to the 'view' page.
	 * @param integer $id the ID of the model to be updated
	 */
	public function actionUpdate($id)
	{
		$model=$this->loadModel($id);

		// Uncomment the following line if AJAX validation is needed
		// $this->performAjaxValidation($model);

		if(isset($_POST['Claim']))
		{
			$model->attributes=$_POST['Claim'];
			if($model->save())
				$this->redirect(array('view','id'=>$model->id));
		}

		$this->render('update',array(
			'model'=>$model,
		));
	}

	/**
	 * Deletes a particular model.
	 * If deletion is successful, the browser will be redirected to the 'index' page.
	 * @param integer $id the ID of the model to be deleted
	 */
	public function actionDelete($id)
	{
		if(Yii::app()->request->isPostRequest)
		{
			// we only allow deletion via POST request
			$this->loadModel($id)->delete();

			// if AJAX request (triggered by deletion via admin grid view), we should not redirect the browser
			if(!isset($_GET['ajax']))
				$this->redirect(isset($_POST['returnUrl']) ? $_POST['returnUrl'] : array('admin'));
		}
		else
			throw new CHttpException(400,'Invalid request. Please do not repeat this request again.');
	}

	/**
	 * Lists all models.
	 */
	public function actionIndex()
	{
		$dataProvider=new CActiveDataProvider('Claim');
		$this->render('index',array(
			'dataProvider'=>$dataProvider,
		));
	}

	/**
	 * Manages all models.
	 */
	public function actionAdmin()
	{
		$model=new Claim('search');
		$model->unsetAttributes();  // clear any default values
		if(isset($_GET['Claim']))
			$model->attributes=$_GET['Claim'];

		$this->render('admin',array(
			'model'=>$model,
		));
	}

	public function actionConsider($id)
	{
		$claim = Claim::model()->findByPk($id);

		if ($claim === null)
			throw new CHttpException(404, "Заявка не найдена");

		if (!$this->allowConsider($claim))
		{
			throw new CHttpException(403, "Доступ запрещен");
		}

		
		$this->render('consider', array('model' => $claim));
	}

	protected function allowConsider(&$claim)
	{
		switch ($claim->type)
		{
			case Claim::TYPE_ADMIN:
				return Yii::app()->user->isAdmin(); 
			case Claim::TYPE_CURATOR:
			case Claim::TYPE_MP:
			case Claim::TYPE_HEAD:
				default: return false;
		}
	}

	/**
	 * Список нерассмотренных заявок администратору
	 */
	public function actionListAdmin()
	{
		$dataProvider = new CActiveDataProvider('ClaimAdmin', array(
			'criteria' => array(
				'condition' => "type=:type AND considered='no'",
				'params' => array(
					':type' => Claim::TYPE_ADMIN
				)
			)
		));
		
		$this->render('listadmin', array(
			'dataProvider' => $dataProvider
		));
	}

	/**
	 * Список рассмотренных заявок администратору
	 */
	public function actionHistoryAdmin()
	{
		throw new CHttpException(404, "Under construction");
	}

	

	/**
	 * Returns the data model based on the primary key given in the GET variable.
	 * If the data model is not found, an HTTP exception will be raised.
	 * @param integer the ID of the model to be loaded
	 */
	public function loadModel($id)
	{
		$model=Claim::model()->findByPk((int)$id);
		if($model===null)
			throw new CHttpException(404,'The requested page does not exist.');
		return $model;
	}

	/**
	 * Performs the AJAX validation.
	 * @param CModel the model to be validated
	 */
	protected function performAjaxValidation($model)
	{
		if(isset($_POST['ajax']) && $_POST['ajax']==='claim-form')
		{
			echo CActiveForm::validate($model);
			Yii::app()->end();
		}
	}
}
