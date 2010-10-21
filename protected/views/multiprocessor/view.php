<?php
$this->breadcrumbs=array(
	'Multiprocessors'=>array('index'),
	$model->name,
);

$this->menu=array(
	array('label'=>'List Multiprocessor', 'url'=>array('index')),
	array('label'=>'Create Multiprocessor', 'url'=>array('create')),
	array('label'=>'Update Multiprocessor', 'url'=>array('update', 'id'=>$model->id)),
	array('label'=>'Delete Multiprocessor', 'url'=>'#', 'linkOptions'=>array('submit'=>array('delete','id'=>$model->id),'confirm'=>'Are you sure you want to delete this item?')),
	array('label'=>'Manage Multiprocessor', 'url'=>array('admin')),
);
?>

<h1>View Multiprocessor #<?php echo $model->id; ?></h1>

<?php $this->widget('zii.widgets.CDetailView', array(
	'data'=>$model,
	'attributes'=>array(
		'id',
		'name',
		'organization_id',
		'public_access',
		'url',
		'support_email',
		'dns_addresses_list',
		'description',
		'status',
		'access_key',
	),
)); ?>
