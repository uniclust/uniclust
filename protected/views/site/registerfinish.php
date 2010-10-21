<div class="form">
	<h1>Завершение регистрации</h1>

	<?php $form=$this->beginWidget('CActiveForm', array(
		'id'=>'register-form',
		'enableAjaxValidation'=>true,
	)); ?>

	<table class="frm" border=0 cellspacing=0 cellpadding=0>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'password'); ?></td>
			<td>
				<?php echo $form->passwordField($model, 'password'); ?>
				<?php echo $form->error($model, 'password'); ?>        
            </td>
			<td>
			</td>
		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'password2'); ?></td>
			<td>
				<?php echo $form->passwordField($model, 'password2'); ?>
				<?php echo $form->error($model, 'password2'); ?>
			</td>
			<td>
				
			</td>
		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'organizationPosition'); ?> &laquo;<?php echo CHtml::encode($orgname); ?>&raquo; </td>
			<td>
				<?php echo $form->textField($model, 'organizationPosition'); ?>
				<?php echo $form->error($model, 'organizationPosition'); ?>
            </td>
			<td>
			</td>

		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'phones'); ?></td>
			<td>
				<?php echo $form->textField($model, 'phones'); ?>
				<?php echo $form->error($model, 'phones'); ?>
			</td>
			<td>
				
			</td>

		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'interests'); ?></td>
			<td>
				<?php echo $form->textArea($model, 'interests'); ?>
				<?php echo $form->error($model, 'interests'); ?>
			</td>
			<td>
			</td>
		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'otherInformation'); ?></td>
			<td>
				<?php echo $form->textArea($model, 'otherInformation'); ?>
				<?php echo $form->error($model, 'otherInformation'); ?>
			</td>
			<td>
			</td>
		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1></td>
			<td>
				<?php echo CHtml::submitButton('Зарегистрироваться'); ?>
			</td>
			<td>
				
			</td>
		</tr>
	</table>
	

	<?php $this->endWidget(); ?>

</div>


