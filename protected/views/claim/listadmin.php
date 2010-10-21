<?php
$this->breadcrumbs=array(
	'Заявки',
);

?>

<h1>Нерассмотренные заявки</h1>

<?php $this->widget('zii.widgets.CListView', array(
	'dataProvider'=>$dataProvider,
	'itemView'=>'_unconsidered',
)); ?>
