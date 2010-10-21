<?php
$this->pageTitle=Yii::app()->name . ' - Вход';
?>

<div class="form" align="center">

	<h1>Вход в систему</h1>

	<?php if(Yii::app()->user->hasFlash('success')): ?>
            <div class="flash-success">
                <?php echo Yii::app()->user->getFlash('success'); ?>
            </div>
    <?php endif; ?>

	<?php $form=$this->beginWidget('CActiveForm', array(
		'id'=>'login-form',
		'enableAjaxValidation'=>true,
	)); ?>
	
	<?php if ($model->hasErrors()): ?>
		<?php echo $form->error($model, 'password'); ?>
	<?php endif; ?>	

	<table class="nav" border="0" cellspacing="4" cellpadding="0" style="background-color: #ccd7e5; padding: 10px">
		<tr>
			<td style="padding-right: 25px"><?php echo $form->labelEx($model, 'username'); ?></td>
			<td><?php echo $form->textField($model, 'username'); ?>
				
			</td>
		</tr>        
		<tr>
			<td style="padding-right: 25px"><?php echo $form->labelEx($model, 'password'); ?></td>
			<td><?php echo $form->passwordField($model, 'password'); ?>
			
			</td>
		</tr>
		<tr>
			<td style="padding-right: 25px"><?php echo $form->checkBox($model,'rememberMe'); ?></td>
			<td><?php echo $form->label($model,'rememberMe'); ?></td>
		</tr>      
		<tr>
			<td colspan="2"><?php echo CHtml::submitButton('Войти'); ?></td>
		</tr>
	</table>
	<?php $this->endWidget(); ?>

	<div style="padding: 15px 10px 2px 10px;">
		<?php echo CHtml::link('Зарегистрироваться', $this->createUrl('/site/register'), array('class' => 'navlink')); ?>
		&bull;
		<?php echo CHtml::link('Забыли пароль?', $this->createUrl('/site/resetpass'), array('class' => 'navlink')); ?>
	</div>

</div>
