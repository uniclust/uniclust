<div class="form">

<?php $form=$this->beginWidget('CActiveForm', array(
	'id'=>'group-form',
	'enableAjaxValidation'=>false,
)); ?>

	<p class="note">Fields with <span class="required">*</span> are required.</p>

	<?php echo $form->errorSummary($model); ?>

	<div class="row">
		<?php echo $form->labelEx($model,'organization_id'); ?>
		<?php echo $form->textField($model,'organization_id',array('size'=>10,'maxlength'=>10)); ?>
		<?php echo $form->error($model,'organization_id'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'group_name'); ?>
		<?php echo $form->textField($model,'group_name',array('size'=>60,'maxlength'=>100)); ?>
		<?php echo $form->error($model,'group_name'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'os_group_name'); ?>
		<?php echo $form->textField($model,'os_group_name',array('size'=>20,'maxlength'=>20)); ?>
		<?php echo $form->error($model,'os_group_name'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'group_description'); ?>
		<?php echo $form->textArea($model,'group_description',array('rows'=>6, 'cols'=>50)); ?>
		<?php echo $form->error($model,'group_description'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'status'); ?>
		<?php echo $form->textField($model,'status',array('size'=>10,'maxlength'=>10)); ?>
		<?php echo $form->error($model,'status'); ?>
	</div>

	<div class="row buttons">
		<?php echo CHtml::submitButton($model->isNewRecord ? 'Create' : 'Save'); ?>
	</div>

<?php $this->endWidget(); ?>

</div><!-- form -->