<div class="form">

<?php $form=$this->beginWidget('CActiveForm', array(
	'id'=>'user-form',
	'enableAjaxValidation'=>false,
)); ?>

	<p class="note">Fields with <span class="required">*</span> are required.</p>

	<?php echo $form->errorSummary($model); ?>

	<div class="row">
		<?php echo $form->labelEx($model,'login'); ?>
		<?php echo $form->textField($model,'login',array('size'=>20,'maxlength'=>20)); ?>
		<?php echo $form->error($model,'login'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'password'); ?>
		<?php echo $form->passwordField($model,'password',array('size'=>60,'maxlength'=>200)); ?>
		<?php echo $form->error($model,'password'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'full_user_name'); ?>
		<?php echo $form->textField($model,'full_user_name',array('size'=>60,'maxlength'=>250)); ?>
		<?php echo $form->error($model,'full_user_name'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'latin_user_name'); ?>
		<?php echo $form->textField($model,'latin_user_name',array('size'=>60,'maxlength'=>250)); ?>
		<?php echo $form->error($model,'latin_user_name'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'phones'); ?>
		<?php echo $form->textField($model,'phones',array('size'=>60,'maxlength'=>250)); ?>
		<?php echo $form->error($model,'phones'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'interests'); ?>
		<?php echo $form->textArea($model,'interests',array('rows'=>6, 'cols'=>50)); ?>
		<?php echo $form->error($model,'interests'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'other_information'); ?>
		<?php echo $form->textArea($model,'other_information',array('rows'=>6, 'cols'=>50)); ?>
		<?php echo $form->error($model,'other_information'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'user_status'); ?>
		<?php echo $form->textField($model,'user_status',array('size'=>10,'maxlength'=>10)); ?>
		<?php echo $form->error($model,'user_status'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'date_of_registration'); ?>
		<?php echo $form->textField($model,'date_of_registration',array('size'=>10,'maxlength'=>10)); ?>
		<?php echo $form->error($model,'date_of_registration'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'primary_email'); ?>
		<?php echo $form->textField($model,'primary_email',array('size'=>60,'maxlength'=>250)); ?>
		<?php echo $form->error($model,'primary_email'); ?>
	</div>

	<div class="row buttons">
		<?php echo CHtml::submitButton($model->isNewRecord ? 'Create' : 'Save'); ?>
	</div>

<?php $this->endWidget(); ?>

</div><!-- form -->