<?php

// Yii::setPathOfAlias('local','path/to/local-folder');

return array(
	'basePath'=>dirname(__FILE__).DIRECTORY_SEPARATOR.'..',
	'name'=>'Unified Cluster Registration System',

	// preloading 'log' component
	'preload'=>array('log'),

	// autoloading model and component classes
	'import'=>array(
		'application.models.*',
		'application.components.*',
		'application.extensions.nestedset.*',
		'application.helpers.*'
	),

	'modules'=>array(
	),	
	
	// application components
	'components'=>array(
		'user'=>array(
			// enable cookie-based authentication
			'allowAutoLogin'=>true,
			'class' => 'WebUser'
		),
		
		'db'=>array(
			'connectionString' => 'mysql:host=localhost;dbname=uniclust',
			'emulatePrepare' => true,
			'username' => 'root',
			'password' => '123456',
			//'tablePrefix' => '',
			'enableParamLogging' => true,
			'charset' => 'utf8',
		),
		
		'errorHandler'=>array(
			// use 'site/error' action to display errors
            'errorAction'=>'site/error',
        ),
		'log'=>array(
			'class'=>'CLogRouter',
			'routes'=>array(
				array(
					'class'=>'CFileLogRoute',
					'levels'=>'error, warning',
				),
				// uncomment the following to show log messages on web pages
				
				array(
					'class'=>'CWebLogRoute',
				),
				
			),
		),

		'authManager' => array(
			'class' => 'PhpAuthManager',
			'defaultRoles' => array('guest'),
		),

		'image' => array(
			'class' => 'application.extensions.image.CImageComponent',
			'driver' => 'GD',
			'params' => '/usr/local/bin'
		),

		'email' => array(
			'class' => 'application.extensions.email.Email',
			'delivery' => 'debug'
		),

		'clientScript' => array(
			'scriptMap' => array(
				//'jquery.js' => 'internal/js/jquery-1.4.2.min.js',
				//'jquery_ui.js' => 'internal/js/jquery_ui/jquery-ui-1.8.4.custom.min.js',

				//'datePicker.css' => 'internal/css/datePicker.css',
				//'jquery_ui.css' => 'internal/css/jquery-ui-1.8.4.custom.css'
			)
		),

		/*
		'urlManager' => array(
			'urlFormat' => 'path',
			'rules' => array(
				'<_c:(login|error|message|locked|underconstruction)>' => 'site/<_c>',
				'<_c:(partner)>' => 'agent',
				'news/<id:\d+>' => 'pflNews/view'
			),
			'baseUrl' => "http://l/pflu",
			'showScriptName' => false
		) */ 
	),

	'params'=>array(
		// this is used in contact page
		'adminEmail'=>'n3xorus@gmail.com',

		'jsUrl' => 'internal/js',
		'cssUrl' => 'internal/css',
		'imgUrl' => 'internal/img',

		'adminEmail'=>'n3xorus@gmail.com',
		'adminLogin' => 'admin',
		'mailer' => 'mailer@uniclust.com'			
	),

	'language' => 'ru'	
);
