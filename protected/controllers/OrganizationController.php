<?php

class OrganizationController extends Controller
{

	public $layout='//layouts/guest';

	public function filters()
	{
		return array(
			'accessControl',
		);
	}

	public function accessRules()
	{
		return array(
			array('allow', 
				'actions'=>array('index','view', 'register'),
				'users'=>array('*'),
			),
			
			array('allow',
				'actions'=>array('create', 'update', 'admin','delete'),
				'users'=>array(Yii::app()->params['adminLogin']),
			),
			array('deny', 
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
		$model=new Organization;

		// Uncomment the following line if AJAX validation is needed
		// $this->performAjaxValidation($model);

		if(isset($_POST['Organization']))
		{
			$model->attributes=$_POST['Organization'];
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

		if(isset($_POST['Organization']))
		{
			$model->attributes=$_POST['Organization'];
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
		$dataProvider=new CActiveDataProvider('Organization');
		$this->render('index',array(
			'dataProvider'=>$dataProvider,
		));
	}

	/**
	 * Manages all models.
	 */
	public function actionAdmin()
	{
		$model=new Organization('search');
		$model->unsetAttributes();  // clear any default values
		if(isset($_GET['Organization']))
			$model->attributes=$_GET['Organization'];

		$this->render('admin',array(
			'model'=>$model,
		));
	}

	/**
	 * Регистрация новой организации
	 * Регистрацию новой организации может осуществить только вновь
	 * регистрирующийся пользователь, который указал в качестве первичной
	 * организации "другая"
	 *
	 * @param string $u
	 * @param string $h
	 * 
	 * @author Pavel Chebotarev
	 */
	public function actionRegister($u, $h)
	{ 
		$pass = PasswordRemind::model()->findByAttributes(
			array(
				'user_id' => $u,
				'hash' => $h
			)
		);

		if ($pass === null)
		{
			throw new CHttpException(403, "Доступ запрещен. Возможно, ваша ссылка устарела");
		}

		$existOrganization = ClaimAdmin::model()->findByAttributes(
			array(
				'user_id' => $u,
				'type' => Claim::TYPE_ADMIN,
				'subtype' => ClaimAdmin::TYPE_NEW_ORG,
				'considered' => 'no'
		));

		if ($existOrganization !== null)
		{ 
			throw new CHttpException(403, "Указанная вами организация ожидает подтверждения администратором");
		}

		$model=new Organization;

		// Uncomment the following line if AJAX validation is needed
		// $this->performAjaxValidation($model);		

		if(isset($_POST['Organization']))
		{
			$model->attributes=$_POST['Organization'];			
			

			if($model->save()) {
				$claim = new ClaimAdmin;
				$claim->subtype = ClaimAdmin::TYPE_NEW_ORG;
				$claim->user_id = Yii::app()->user->id;
				$claim->target_id = $model->id;
				$claim->is_primary = 'yes';
				$claim->user_id = $u;
				
				if (!$claim->save())
				{
					var_dump($claim->getErrors());
					die("Claim not saved");
				}

				$uRel = new  UserOrganizationRelation;
				$uRel->user_id = $u;
				$uRel->organization_id = $model->id;
				$uRel->is_primary = 'yes';
				$uRel->position = '';
				if (!$uRel->save()) {
					var_dump($uRel->getErrors());
					die('user_relation not saved');
				}
				
				Yii::app()->user->setFlash('success', "Организация зарегистрирована. После подтверждения статуса организации администратором, в нее смогут вступать другие пользователи");
				$this->redirect($this->createUrl('/site/registerfinish', array('u'=>$u, 'h'=>$h)));
			}
		}

		$this->render('register',array(
			'model'=>$model,
		));
	}

	public function loadModel($id)
	{
		$model=Organization::model()->findByPk((int)$id);
		if($model===null)
			throw new CHttpException(404,'The requested page does not exist.');
		return $model;
	}

	protected function performAjaxValidation($model)
	{
		if(isset($_POST['ajax']) && $_POST['ajax']==='organization-form')
		{
			echo CActiveForm::validate($model);
			Yii::app()->end();
		}
	}
}
