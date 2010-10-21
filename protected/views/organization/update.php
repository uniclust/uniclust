<?php
$this->breadcrumbs=array(
	'Организации'=>array('admin'),
	$model->id=>array('view','id'=>$model->id),
	'Редактирование',
);

$this->menu=array(
	array('label'=>'Список орагинзаций', 'url'=>array('admin')),
	array('label'=>'Создать организацию', 'url'=>array('create')),
	array('label'=>'Просмотр организации', 'url'=>array('view', 'id'=>$model->id))
);
?>

<h1>Редактировать организацию <?php echo $model->id; ?></h1>

<?php echo $this->renderPartial('_form', array('model'=>$model)); ?>
