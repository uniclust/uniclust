<?php
$this->breadcrumbs=array(
	'Multiprocessors',
);

$this->menu=array(
	array('label'=>'Create Multiprocessor', 'url'=>array('create')),
	array('label'=>'Manage Multiprocessor', 'url'=>array('admin')),
);
?>

<h1>Multiprocessors</h1>

<?php $this->widget('zii.widgets.CListView', array(
	'dataProvider'=>$dataProvider,
	'itemView'=>'_view',
)); ?>
