<?php $this->beginContent('//layouts/main'); ?>
<div id="nav">
<?php $this->widget('zii.widgets.CMenu', array(
				'items'=>$this->menu,
				'htmlOptions'=>array('class'=>'operations'),
			)); ?>
</div>
			<?php echo $content; ?>
		
<?php $this->endContent(); ?>
