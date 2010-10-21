<div class="view">

	<b><?php echo CHtml::encode($data->getAttributeLabel('id')); ?>:</b>
	<?php echo CHtml::link(CHtml::encode($data->id), array('view', 'id'=>$data->id)); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('date')); ?>:</b>
	<?php echo CHtml::encode($data->date); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('type')); ?>:</b>
	<?php echo CHtml::encode($data->type); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('subtype')); ?>:</b>
	<?php echo CHtml::encode($data->subtype); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('user_id')); ?>:</b>
	<?php echo CHtml::encode($data->user_id); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('target_id')); ?>:</b>
	<?php echo CHtml::encode($data->target_id); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('is_primary')); ?>:</b>
	<?php echo CHtml::encode($data->is_primary); ?>
	<br />

	<?php /*
	<b><?php echo CHtml::encode($data->getAttributeLabel('param1')); ?>:</b>
	<?php echo CHtml::encode($data->param1); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('param2')); ?>:</b>
	<?php echo CHtml::encode($data->param2); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('data')); ?>:</b>
	<?php echo CHtml::encode($data->data); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('considered')); ?>:</b>
	<?php echo CHtml::encode($data->considered); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('considered_by')); ?>:</b>
	<?php echo CHtml::encode($data->considered_by); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('consideration_date')); ?>:</b>
	<?php echo CHtml::encode($data->consideration_date); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('reason')); ?>:</b>
	<?php echo CHtml::encode($data->reason); ?>
	<br />

	*/ ?>

	<?php echo CHtml::link('Рассмотреть  заявку', $this->createUrl('/claim/consider', array('id' => $data->id))); ?>

</div>
