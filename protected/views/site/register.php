<div class="form">
	<h1>Регистрация</h1>

	<?php $form=$this->beginWidget('CActiveForm', array(
		'id'=>'login-form',
		'enableAjaxValidation'=>false,
	)); ?>

	<table class="frm" border=0 cellspacing=0 cellpadding=0>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'full_user_name'); ?></td>
			<td>
				<?php echo $form->textField($model, 'full_user_name'); ?>
				<?php echo $form->error($model, 'full_user_name'); ?>        
            </td>
			<td>Фамилия, имя, отчество.
			</td>
		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'latin_user_name'); ?></td>
			<td>
				<?php echo $form->textField($model, 'latin_user_name'); ?>
				<?php echo $form->error($model, 'latin_user_name'); ?>
			</td>
			<td>
				
			</td>
		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'login'); ?></td>
			<td>
				<?php echo $form->textField($model, 'login'); ?>
				<?php echo $form->error($model, 'login'); ?>
            </td>
			<td>
				Желаемый логин для входа в систему.
			</td>

		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'primary_email'); ?></td>
			<td>
				<?php echo $form->textField($model, 'primary_email'); ?>
				<?php echo $form->error($model, 'primary_email'); ?>
			</td>
			<td>
				Необходим реальный, действующий адрес.
			</td>

		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'primaryOrganization'); ?></td>
			<td>
				<?php echo $form->dropDownList($model, 'primaryOrganization', $organizations,
				array(
					'empty' => ' - ',
				)
				); ?>
				<?php echo $form->error($model, 'primaryOrganization'); ?>
			</td>
			<td>
				Выберите организацию из списка.  Если нужной организации нет в списке, выберите "Другая"
			</td>
		</tr>
		<tr><td colspan=3><hr/></td></tr>
		<tr>
			<td nowrap=1></td>
			<td>
				<?php echo CHtml::submitButton('Вперед'); ?>
			</td>
			<td>
				
			</td>
		</tr>
	</table>
	

	<?php $this->endWidget(); ?>

</div>


