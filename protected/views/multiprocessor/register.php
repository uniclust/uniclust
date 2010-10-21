<div class="form">
	<h1>Регистрация многопроцессорной системы</h1>

	<?php $form=$this->beginWidget('CActiveForm', array(
		'id'=>'login-form',
		'enableAjaxValidation'=>false,
	)); ?>

	<table class="frm" border=0 cellspacing=0 cellpadding=0>
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'orgId'); ?></td>
			<td>
				<?php echo $form->dropDownList($model, 'orgId', $organizationsList,
				array(
					'empty' => ' - '
				)); ?>
				<?php echo $form->error($model, 'orgId'); ?>        
            </td>
			<td>Выберите организацию, которой принадлежит регистрируемая МС
			</td>
		</tr>
		
		<tr><td colspan=3><hr/></td></tr>

		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'name'); ?></td>
			<td>
				<?php echo $form->textField($model, 'name'); ?>
				<?php echo $form->error($model, 'name'); ?>
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
			</td>
		</tr>
		
		<tr><td colspan=3><hr/></td></tr>

		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'url'); ?></td>
			<td>
				<?php echo $form->textField($model, 'url'); ?>
				<?php echo $form->error($model, 'url'); ?>
			</td>
			<td>
			</td>

		</tr>
		<tr><td colspan=3><hr/></td></tr>

		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'supportEmail'); ?></td>
			<td>
				<?php echo $form->textField($model, 'supportEmail'); ?>
				<?php echo $form->error($model, 'supportEmail'); ?>
			</td>
			<td>
			</td>
		</tr>
		<tr><td colspan=3><hr/></td></tr>
		
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'publicAccess'); ?></td>
			<td>
				<?php echo $form->checkBox($model, 'publicAccess'); ?>
				<?php echo $form->error($model, 'publicAccess'); ?>
			</td>
			<td>
			</td>

		</tr>
		<tr><td colspan=3><hr/></td></tr>

		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'dnsAddressesList'); ?></td>
			<td>
				<?php echo $form->textArea($model, 'dnsAddressesList'); ?>
				<?php echo $form->error($model, 'dnsAddressesList'); ?>
			</td>
			<td>
			</td>
		</tr>
		<tr><td colspan=3><hr/></td></tr>
		
		<tr>
			<td nowrap=1><?php echo $form->labelEx($model, 'description'); ?></td>
			<td>
				<?php echo $form->textArea($model, 'description'); ?>
				<?php echo $form->error($model, 'description'); ?>
			</td>
			<td>
				Предназначение МС, число и тип процессоров, тип коммуникационной среды, операционная система, предполагаемая производительность (в терафлопах)
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


