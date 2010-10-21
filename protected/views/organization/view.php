<?php
$this->breadcrumbs=array(
	'Организации'=>array('index'),
	$model->id,
);

$this->menu=array(
	array('label'=>'List Organization', 'url'=>array('index')),
	array('label'=>'Create Organization', 'url'=>array('create')),
	array('label'=>'Update Organization', 'url'=>array('update', 'id'=>$model->id)),
	array('label'=>'Delete Organization', 'url'=>'#', 'linkOptions'=>array('submit'=>array('delete','id'=>$model->id),'confirm'=>'Are you sure you want to delete this item?')),
	array('label'=>'Manage Organization', 'url'=>array('admin')),
);
?>

<h1>View Organization #<?php echo $model->id; ?></h1>

<?php $this->widget('zii.widgets.CDetailView', array(
	'data'=>$model,
	'attributes'=>array(
		'id',
		'russian_short_name',
		'english_short_name',
		'full_name',
		'url',
		'organization_description',
		'phone',
		'address',
		'head',
		'status',
	),
)); ?>
