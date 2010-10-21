<?php

class SiteController extends Controller
{
	public $layout = '//layouts/guest';
	/**
	 * Declares class-based actions.
	 */
	public function actions()
	{
		return array(
			// captcha action renders the CAPTCHA image displayed on the contact page
			'captcha'=>array(
				'class'=>'CCaptchaAction',
				'backColor'=>0xFFFFFF,
			),
			// page action renders "static" pages stored under 'protected/views/site/pages'
			// They can be accessed via: index.php?r=site/page&view=FileName
			'page'=>array(
				'class'=>'CViewAction',
			),
		);
	}

	public function beforeAction($action)
	{
		if (!Yii::app()->user->isGuest)
		{
			$this->layout = '//layouts/main';
		}
		return parent::beforeAction($action);
	}

	public function filters()
	{
		return array(
			'accessControl', // perform access control for CRUD operations
		);
	}


	public function accessRules()
	{
		return array(
			array('allow', 
				'actions'=>array('register', 'regsaved', 'registerfinish', 'login', 'contact', 'error'),
				'users'=>array('*'),
			),
			array('allow', 
				'users'=>array('@'),
			),
			
			array('deny',  // deny all users
				'users'=>array('*'),
			),
		);
	}

	/**
	 * This is the default 'index' action that is invoked
	 * when an action is not explicitly requested by users.
	 */
	public function actionIndex()
	{
		$this->layout = '//layouts/main';

		$organizations = UserOrganizationRelation::model()->with('organization')->findAllByAttributes(array('user_id' => Yii::app()->user->id));

		
		$this->render('index', array(
			'organizations' => $organizations,
			
		));
	}

	public function actionRegister()
	{
		$organizations = Organization::model()->findAllByAttributes(array('status' => 'registered'));
		$organizations = CHtml::listData($organizations, 'id', 'russian_short_name');
		$organizations += array('-1' => '(Другая)');

		$model = new UserRegistrationForm;

		if (isset($_POST['UserRegistrationForm']))
		{			
			$model->attributes = $_POST['UserRegistrationForm'];
			
			$userExists = User::model()->findByAttributes(array('login' => $model->login));
			
			if ($userExists !== null)
			{
				$model->addError('login', 'Выбранный логин уже занят.  Пожалуйста, выберите другой логин');
				$this->render('register', array(
					'model' => $model,
					'organizations' => $organizations
				));
				Yii::app()->end();
			}
			
			if ($model->primaryOrganization)
			{
				$organization = Organization::model()->findByPk($model->primaryOrganization);
				if ($organization === null)
				{
					$model->addError('primaryOrganization', 'Неверно указана организация');
				} else {
					$relOrg = new UserOrganizationRelation;
					$relOrg->is_primary = 'yes';
					$relOrg->organization_id = $model->primaryOrganization;
				}
			}

			$passwordRemind = new PasswordRemind;
			
			if ($model->validate())
			{
				$transaction = Yii::app()->db->beginTransaction();
				try {   
					
						if (!$model->save())
						{
							throw new Exception("Model not saved");
						}
								
						if (isset($relOrg))
						{
							$relOrg->user_id = $model->id;
							if (!$relOrg->save())
							{
								throw new Exception("UserOrganizationRelation save failed");
							}
						}
						
						$passwordRemind = new PasswordRemind;
						$passwordRemind->user_id = $model->id;
						$passwordRemind->register = 'yes';
						
						if(!$passwordRemind->save())
						{
							throw new Exception("PasswordRemind save failed");
						}
							
						$transaction->commit();
		
				} catch (Exception $e) {
					$transaction->rollback();
					throw $e;
				}

				Yii::app()->session['userid'] = $model->id;
				Yii::app()->session['neworg'] = !isset($relOrg);
				$this->redirect($this->createUrl('/site/regsaved'));			
			}		
		}
		Yii::app()->session['userid'] = null;
		Yii::app()->session['neworg'] = null;

		$this->render('register', array(
			'model' => $model,
			'organizations' => $organizations
		));
	}

	public function actionRegsaved() {
		if (!Yii::app()->session['userid'])
		{
			$this->redirect($this->createUrl('/site/register'));
		}
		
		$user = User::model()->findByPk(Yii::app()->session['userid']);
		$passwordRemind = PasswordRemind::model()->findByAttributes(array('user_id' => $user->id));
		
		$email = Yii::app()->email;
		$email->to = $user->primary_email;
		$email->from = 'mailer@uniclust.ru';
		$email->subject = 'Подтвержение регистрации на сайте Uniclust';
		$params = array(
			'hash' => $passwordRemind->hash,
			'neworg' => Yii::app()->session['neworg'],
			'userid' => $user->id
		);
		$email->message = $this->renderPartial('/site/mail/register', $params, true);
		$email->send();
		$this->render('regsaved');
	}

	public function actionRegisterFinish($u, $h)
	{
		$pass = PasswordRemind::model()->findByAttributes(
			array(
				'user_id' => $u,
				'hash' => $h
			)
		);

		if ($pass === null)
		{
			throw new CHttpException(404, "Страница не найдена. Возможно, Ваша ссылка устарела");
		} 

		$userOrganizationRelation = UserOrganizationRelation::model()->findByAttributes(
			array(
				'user_id' => $u,
				'is_primary' => 'yes'
			)
		);

		if ($userOrganizationRelation === null)
		{
			$this->redirect($this->createUrl('/organization/register', array(
				'u' => $u,
				'h' => $h
			)));
		}

		$model = new UserRegistrationFinishForm;

		if (isset($_POST['UserRegistrationFinishForm']))
		{
			$model->attributes = $_POST['UserRegistrationFinishForm'];
			if ($model->validate())
			{
				$userOrganizationRelation->position = $model->organizationPosition;
				//$pass->delete();

				$user = User::model()->findByPk($u);
				$user->user_status = 'registered';
				$user->password = UserIdentity::hashPassword($model->password);
				$user->phones = $model->phones;
				$user->interests = $model->interests;
				$user->other_information = $model->otherInformation;
				$user->save() || die('user not saved');

				Yii::app()->user->setFlash('success', "Регистрация успешно завершена! Используйте Ваш логин и пароль для входа");
				$this->redirect($this->createUrl('/site/login'));
			}
		}
		
		$this->render('registerfinish', array(
			'model' => $model,
			'orgname' => $userOrganizationRelation->organization->russian_short_name
		));
	}

	/**
	 * This is the action to handle external exceptions.
	 */
	public function actionError()
	{
	    if($error=Yii::app()->errorHandler->error)
	    {
	    	if(Yii::app()->request->isAjaxRequest)
	    		echo $error['message'];
	    	else
	        	$this->render('error', $error);
	    }
	}

	/**
	 * Displays the contact page
	 */
	public function actionContact()
	{
		$model=new ContactForm;
		if(isset($_POST['ContactForm']))
		{
			$model->attributes=$_POST['ContactForm'];
			if($model->validate())
			{
				$headers="From: {$model->email}\r\nReply-To: {$model->email}";
				mail(Yii::app()->params['adminEmail'],$model->subject,$model->body,$headers);
				Yii::app()->user->setFlash('contact','Thank you for contacting us. We will respond to you as soon as possible.');
				$this->refresh();
			}
		}
		$this->render('contact',array('model'=>$model));
	}

	/**
	 * Displays the login page
	 */
	public function actionLogin()
	{
		$this->layout = '//layouts/guest';
		$model=new LoginForm;

		// if it is ajax validation request
		if(isset($_POST['ajax']) && $_POST['ajax']==='login-form')
		{
			echo CActiveForm::validate($model);
			Yii::app()->end();
		}

		// collect user input data
		if(isset($_POST['LoginForm']))
		{
			$model->attributes=$_POST['LoginForm'];
			// validate user input and redirect to the previous page if valid
			if($model->validate() && $model->login())
				$this->redirect(Yii::app()->user->returnUrl);
		}
		// display the login form
		$this->render('login',array('model'=>$model));
	}

	/**
	 * Logs out the current user and redirect to homepage.
	 */
	public function actionLogout()
	{
		Yii::app()->user->logout();
		$this->redirect(Yii::app()->homeUrl);
	}

	/**
	 * Страница администрирования
	 */
	public function actionAdmin()
	{
		$cmd = Yii::app()->db->createCommand(
			"SELECT COUNT(*) FROM {{claims}} WHERE type=:type AND considered = 'no'"
		);
		$cmd->bindValue(':type', Claim::TYPE_ADMIN);
		$claimsCount = $cmd->queryScalar();
		
		$this->render('admin', array(
			'claimsCount' => $claimsCount
		));
	}
}
