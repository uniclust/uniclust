<div class="form">



<?php $form=$this->beginWidget('CActiveForm', array(
	'id'=>'claim-form',
	'enableAjaxValidation'=>false,
)); ?>

	<p class="note">Fields with <span class="required">*</span> are required.</p>

	<?php echo $form->errorSummary($model); ?>

	<div class="row">
		<?php echo $form->labelEx($model,'date'); ?>
		<?php echo $form->textField($model,'date'); ?>
		<?php echo $form->error($model,'date'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'type'); ?>
		<?php echo $form->textField($model,'type',array('size'=>7,'maxlength'=>7)); ?>
		<?php echo $form->error($model,'type'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'subtype'); ?>
		<?php echo $form->textField($model,'subtype',array('size'=>50,'maxlength'=>50)); ?>
		<?php echo $form->error($model,'subtype'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'user_id'); ?>
		<?php echo $form->textField($model,'user_id',array('size'=>10,'maxlength'=>10)); ?>
		<?php echo $form->error($model,'user_id'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'target_id'); ?>
		<?php echo $form->textField($model,'target_id',array('size'=>10,'maxlength'=>10)); ?>
		<?php echo $form->error($model,'target_id'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'is_primary'); ?>
		<?php echo $form->textField($model,'is_primary',array('size'=>60,'maxlength'=>100)); ?>
		<?php echo $form->error($model,'is_primary'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'param1'); ?>
		<?php echo $form->textField($model,'param1',array('size'=>60,'maxlength'=>100)); ?>
		<?php echo $form->error($model,'param1'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'param2'); ?>
		<?php echo $form->textField($model,'param2',array('size'=>60,'maxlength'=>100)); ?>
		<?php echo $form->error($model,'param2'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'data'); ?>
		<?php echo $form->textArea($model,'data',array('rows'=>6, 'cols'=>50)); ?>
		<?php echo $form->error($model,'data'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'considered'); ?>
		<?php echo $form->textField($model,'considered',array('size'=>11,'maxlength'=>11)); ?>
		<?php echo $form->error($model,'considered'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'considered_by'); ?>
		<?php echo $form->textField($model,'considered_by',array('size'=>10,'maxlength'=>10)); ?>
		<?php echo $form->error($model,'considered_by'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'consideration_date'); ?>
		<?php echo $form->textField($model,'consideration_date'); ?>
		<?php echo $form->error($model,'consideration_date'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'reason'); ?>
		<?php echo $form->textArea($model,'reason',array('rows'=>6, 'cols'=>50)); ?>
		<?php echo $form->error($model,'reason'); ?>
	</div>

	<div class="row buttons">
		<?php echo CHtml::submitButton($model->isNewRecord ? 'Create' : 'Save'); ?>
	</div>

<?php $this->endWidget(); ?>

</div><!-- form -->
