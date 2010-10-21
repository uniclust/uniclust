<?php
$this->breadcrumbs=array(
	'Multiprocessors'=>array('index'),
	'Create',
);

$this->menu=array(
	array('label'=>'List Multiprocessor', 'url'=>array('index')),
	array('label'=>'Manage Multiprocessor', 'url'=>array('admin')),
);
?>

<h1>Create Multiprocessor</h1>

<?php echo $this->renderPartial('_form', array('model'=>$model)); ?>