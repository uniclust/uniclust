<table border=0 cellspacing=0 cellpadding=0 width="100%">
<tr>
<td valign="top" style="padding-right: 15px" width="50%">
	<h3>Заявки</h3>
	<ul>
		<li><?php if ($claimsCount) {
			echo '<b>'.CHtml::link('Нерассмотренные заявки ('.$claimsCount.')', $this->createUrl('/claim/listadmin')).'</b>';
			 } else {
			echo 'Нерассмотренные заявки';
		} ?></li>
		<li><?php echo CHtml::link('История заявок', $this->createUrl('/claim/historyadmin')); ?></li>
	</ul>
	
    <h3>Организации</h3>
    <ul>
        <li /><?php echo CHtml::link('Создать организацию', $this->createUrl('/organization/create'));?>
        <li /><?php echo CHtml::link('Список организаций', $this->createUrl('/organization/admin'));?>
    </ul>

    <br />

    <h3>Мультипроцессорные системы</h3>
    <ul>
		<li /> <?php echo CHtml::link('Создать МС', $this->createUrl('/multiprocessor/create')); ?>
        <li/> <?php echo CHtml::link('Список МС', $this->createUrl('/multiprocessor/admin')); ?>
    </ul>

    <br />

	<h3>Пользователи</h3>
    <ul>
		<li /> <?php echo CHtml::link('Создать пользователя', $this->createUrl('/user/create')); ?>
        <li/> <?php echo CHtml::link('Список пользователей', $this->createUrl('/user/admin')); ?>
    </ul>

    <br />
    
    <h3>Группы</h3>
    <ul>
    
    </ul>
    
    
