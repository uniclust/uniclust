<?php
$this->breadcrumbs=array(
	'Claims'=>array('index'),
	$model->id,
);

$this->menu=array(
	array('label'=>'List Claim', 'url'=>array('index')),
	array('label'=>'Create Claim', 'url'=>array('create')),
	array('label'=>'Update Claim', 'url'=>array('update', 'id'=>$model->id)),
	array('label'=>'Delete Claim', 'url'=>'#', 'linkOptions'=>array('submit'=>array('delete','id'=>$model->id),'confirm'=>'Are you sure you want to delete this item?')),
	array('label'=>'Manage Claim', 'url'=>array('admin')),
);
?>

<h1>View Claim #<?php echo $model->id; ?></h1>

<?php $this->widget('zii.widgets.CDetailView', array(
	'data'=>$model,
	'attributes'=>array(
		'id',
		'date',
		'type',
		'subtype',
		'user_id',
		'target_id',
		'is_primary',
		'param1',
		'param2',
		'data',
		'considered',
		'considered_by',
		'consideration_date',
		'reason',
	),
)); ?>
