<h1>Регистрация новой организации</h1>

<div class="form">

<?php $form=$this->beginWidget('CActiveForm', array(
	'id'=>'organization-form',
	'enableAjaxValidation'=>false,
)); ?>

	<p class="note">Поля с <span class="required">*</span> обязательны для заполнения.</p>

	<?php echo $form->errorSummary($model); ?>

	<div class="row">
		<?php echo $form->labelEx($model,'russian_short_name'); ?>
		<?php echo $form->textField($model,'russian_short_name',array('size'=>30,'maxlength'=>30)); ?>
		<?php echo $form->error($model,'russian_short_name'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'english_short_name'); ?>
		<?php echo $form->textField($model,'english_short_name',array('size'=>30,'maxlength'=>30)); ?>
		<?php echo $form->error($model,'english_short_name'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'full_name'); ?>
		<?php echo $form->textField($model,'full_name',array('size'=>60,'maxlength'=>200)); ?>
		<?php echo $form->error($model,'full_name'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'url'); ?>
		<?php echo $form->textField($model,'url',array('size'=>60,'maxlength'=>250)); ?>
		<?php echo $form->error($model,'url'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'organization_description'); ?>
		<?php echo $form->textArea($model,'organization_description',array('rows'=>6, 'cols'=>50)); ?>
		<?php echo $form->error($model,'organization_description'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'phone'); ?>
		<?php echo $form->textField($model,'phone',array('size'=>60,'maxlength'=>100)); ?>
		<?php echo $form->error($model,'phone'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'address'); ?>
		<?php echo $form->textArea($model,'address',array('rows'=>6, 'cols'=>50)); ?>
		<?php echo $form->error($model,'address'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model, 'head'); ?>
		<?php echo $form->textField($model, 'head', array('size' => 50)); ?>
		<?php echo $form->error($model, 'head'); ?>
	</div>

	<div class="row buttons">
		<?php echo CHtml::submitButton('Отправить заявку'); ?>
	</div>

<?php $this->endWidget(); ?>

</div><!-- form -->
