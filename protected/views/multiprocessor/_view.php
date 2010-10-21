<div class="view">

	<b><?php echo CHtml::encode($data->getAttributeLabel('id')); ?>:</b>
	<?php echo CHtml::link(CHtml::encode($data->id), array('view', 'id'=>$data->id)); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('name')); ?>:</b>
	<?php echo CHtml::encode($data->name); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('organization_id')); ?>:</b>
	<?php echo CHtml::encode($data->organization_id); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('public_access')); ?>:</b>
	<?php echo CHtml::encode($data->public_access); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('url')); ?>:</b>
	<?php echo CHtml::encode($data->url); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('support_email')); ?>:</b>
	<?php echo CHtml::encode($data->support_email); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('dns_addresses_list')); ?>:</b>
	<?php echo CHtml::encode($data->dns_addresses_list); ?>
	<br />

	<?php /*
	<b><?php echo CHtml::encode($data->getAttributeLabel('description')); ?>:</b>
	<?php echo CHtml::encode($data->description); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('status')); ?>:</b>
	<?php echo CHtml::encode($data->status); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('access_key')); ?>:</b>
	<?php echo CHtml::encode($data->access_key); ?>
	<br />

	*/ ?>

</div>