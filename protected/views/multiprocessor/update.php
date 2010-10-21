<?php
$this->breadcrumbs=array(
	'Multiprocessors'=>array('index'),
	$model->name=>array('view','id'=>$model->id),
	'Update',
);

$this->menu=array(
	array('label'=>'List Multiprocessor', 'url'=>array('index')),
	array('label'=>'Create Multiprocessor', 'url'=>array('create')),
	array('label'=>'View Multiprocessor', 'url'=>array('view', 'id'=>$model->id)),
	array('label'=>'Manage Multiprocessor', 'url'=>array('admin')),
);
?>

<h1>Update Multiprocessor <?php echo $model->id; ?></h1>

<?php echo $this->renderPartial('_form', array('model'=>$model)); ?>