<div class="view">

	<b><?php echo CHtml::encode($data->getAttributeLabel('id')); ?>:</b>
	<?php echo CHtml::link(CHtml::encode($data->id), array('view', 'id'=>$data->id)); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('login')); ?>:</b>
	<?php echo CHtml::encode($data->login); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('password')); ?>:</b>
	<?php echo CHtml::encode($data->password); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('full_user_name')); ?>:</b>
	<?php echo CHtml::encode($data->full_user_name); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('latin_user_name')); ?>:</b>
	<?php echo CHtml::encode($data->latin_user_name); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('phones')); ?>:</b>
	<?php echo CHtml::encode($data->phones); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('interests')); ?>:</b>
	<?php echo CHtml::encode($data->interests); ?>
	<br />

	<?php /*
	<b><?php echo CHtml::encode($data->getAttributeLabel('other_information')); ?>:</b>
	<?php echo CHtml::encode($data->other_information); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('user_status')); ?>:</b>
	<?php echo CHtml::encode($data->user_status); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('date_of_registration')); ?>:</b>
	<?php echo CHtml::encode($data->date_of_registration); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('primary_email')); ?>:</b>
	<?php echo CHtml::encode($data->primary_email); ?>
	<br />

	*/ ?>

</div>