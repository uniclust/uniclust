<?php
$this->breadcrumbs=array(
	'Организации'=>array('admin'),
	'Создать',
);

$this->menu=array(
	array('label'=>'Список организаций', 'url'=>array('admin'))
);
?>

<h1>Создать организацию</h1>

<?php echo $this->renderPartial('_form', array('model'=>$model)); ?>
