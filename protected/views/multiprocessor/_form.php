<div class="form">

<?php $form=$this->beginWidget('CActiveForm', array(
	'id'=>'multiprocessor-form',
	'enableAjaxValidation'=>false,
)); ?>

	<p class="note">Fields with <span class="required">*</span> are required.</p>

	<?php echo $form->errorSummary($model); ?>

	<div class="row">
		<?php echo $form->labelEx($model,'name'); ?>
		<?php echo $form->textField($model,'name',array('size'=>20,'maxlength'=>20)); ?>
		<?php echo $form->error($model,'name'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'organization_id'); ?>
		<?php echo $form->textField($model,'organization_id',array('size'=>10,'maxlength'=>10)); ?>
		<?php echo $form->error($model,'organization_id'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'public_access'); ?>
		<?php echo $form->textField($model,'public_access',array('size'=>3,'maxlength'=>3)); ?>
		<?php echo $form->error($model,'public_access'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'url'); ?>
		<?php echo $form->textField($model,'url',array('size'=>60,'maxlength'=>250)); ?>
		<?php echo $form->error($model,'url'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'support_email'); ?>
		<?php echo $form->textField($model,'support_email',array('size'=>60,'maxlength'=>100)); ?>
		<?php echo $form->error($model,'support_email'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'dns_addresses_list'); ?>
		<?php echo $form->textField($model,'dns_addresses_list',array('size'=>60,'maxlength'=>250)); ?>
		<?php echo $form->error($model,'dns_addresses_list'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'description'); ?>
		<?php echo $form->textArea($model,'description',array('rows'=>6, 'cols'=>50)); ?>
		<?php echo $form->error($model,'description'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'status'); ?>
		<?php echo $form->textField($model,'status',array('size'=>10,'maxlength'=>10)); ?>
		<?php echo $form->error($model,'status'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'access_key'); ?>
		<?php echo $form->textField($model,'access_key',array('size'=>32,'maxlength'=>32)); ?>
		<?php echo $form->error($model,'access_key'); ?>
	</div>

	<div class="row buttons">
		<?php echo CHtml::submitButton($model->isNewRecord ? 'Create' : 'Save'); ?>
	</div>

<?php $this->endWidget(); ?>

</div><!-- form -->