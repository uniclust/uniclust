<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>

    <?php echo CHtml::cssFile(Yii::app()->request->baseUrl.'/css/main.css'); ?>
    <?php echo CHtml::cssFile(Yii::app()->request->baseUrl.'/css/form.css'); ?>

    <title><?php echo CHtml::encode($this->pageTitle); ?></title>
</head>
<body>
   <div style="margin-bottom: 5px">
    <table border="0" width="100%" cellpadding="10" cellspacing=0>
      <tr>
        <td style="padding-top: 5px; padding-left: 15px">
            <a href="<?php echo $this->createUrl('/site');?>">
                <img border="0" width="120" height="107" alt="logo" src="img/logo.png">
            </a>
        </td>
        <td align="right">
            <?php echo CHtml::link('Выход ('.CHtml::encode(Yii::app()->user->login).')', $this->createUrl('/site/logout'),
				array(
					'class' => 'navlink'
				)
            ); ?> 
        </td>
        
      </tr>
      <tr>
         <td valign="bottom" width="*" nowrap colspan="2" align="center">
            <?php echo CHtml::link('Главная', $this->createAbsoluteUrl('/'), array(
				'class' => 'navlink'
            )); ?> &nbsp;&nbsp;
			<?php echo CHtml::link('Обратная связь', $this->createUrl('/site/contact'), array(
				'class' => 'navlink'
			)); ?>
			<?php if (Yii::app()->user->isAdmin()) {
				echo CHtml::link('Панель администрирования', $this->createUrl('/site/admin'), array(
					'class' => 'navlink'
				));
			} ?>                             
        </td>
      </tr>
    </table>
</div>
<hr>
<table border="0" cellspacing=0 cellpadding=0 width="100%">
  <tr>
	<td style="padding: 0px 10px 0px 10px" valign="top" width="100%">
		<?php $this->widget('zii.widgets.CBreadcrumbs', array(
		'links'=>$this->breadcrumbs,
	)); ?><!-- breadcrumbs -->
	</td>
  </tr>	
  <tr>
    <td style="padding: 10px 10px 10px 10px" valign="top" width="100%">
    
    <!-- {include file="systemmessage.tpl"} -->

    <?php echo $content; ?>
    </td>

  </tr>
</table> 
</body>
</html>
