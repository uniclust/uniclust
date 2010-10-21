<table border=0 cellspacing=0 cellpadding=0 width="100%">
<tr>
<td valign="top" style="padding-right: 15px" width="50%">
    <h3>Личные данные</h3>
    <ul>
        <li /><?php echo CHtml::link('Информация о себе', $this->createUrl('/user/edit'));?>
        <li /><?php echo CHtml::link('Адреса электронной почты', $this->createUrl('/user/editemails'));?>
    </ul>

    <br />

    <h3>Организации</h3>
    <ul>
        <?php foreach($organizations as $org): ?>
        <li/>
        <?php echo CHtml::link($org->organization->russian_short_name, $this->createUrl('/organization/info', array('id' => $org->organization_id))); ?>, 
        <span title="<?php echo UserOrganizationRelation::$statusHelps[$org->status]; ?>" style="font-size: 8pt; color: #565656"><?php echo CHtml::encode(UserOrganizationRelation::$statusNames[$org->status]); ?></span>
        <?php echo Chtml::encode($org->position);?>
        <?php endforeach; ?>
    </ul>
    <ul>
        <li /><?php echo CHtml::link('Вступить в организацию', $this->createUrl('/organization/join'), array(
			'style' => "color: #666666; font-size: 80%;"
        )); ?>
    </ul>

    <br />
    <h3>Группы</h3>
    <ul> <?php /**
        {foreach from=$grouplist key=group_id item=group}
            <li/>
            <a href="info/group.php?id={$group_id}">{$group->group_name|escape}</a>
            <span title="{$group->help|escape}" style="font-size: 8pt; color: #565656">{$group->status}</span>
			
			{if $group->user_status=='head'}
			<ul>
				<li>
						<a href="adm_gr_head/claims.php?gr={$group_id}">Заявки ({$group->claims})</a>
				</li>
				<li>
						<a href="adm_gr_head/request_list.php?gr={$group_id}">Заявления для организаций</a>
				</li>
				<li>
						<a href="adm_gr_head/mp_add.php?gr={$group_id}" title="Зарегистрировать группу на многопроцесорной системе">Регистрация на МС</a>
				</li>
				<li>
					 <!--   <a href="adm_mp/claim_history.php">История заявок</a> -->
				</li>
			</ul> 
			{/if}
        {/foreach} **/ ?>
    </ul>
    <ul>
        <li /><a style="color: #666666; font-size: 80%;" href="membership/join_group.php">Вступить в группу</a>  
    </ul>
    <ul>
    <li /> <?php echo CHtml::link('Создать группу', $this->createUrl('/multiprocessor/register'), array(
		'style' => "color: #666666; font-size: 80%;" 
    ));
          
    </ul>
<?php /**
	{if count($curgroups)}
	<h3>Курирование групп</h3>
	<ul>
		{foreach from=$curgroups item=group}
			{if $group->invite}
			{include file="adm_cur/invite.tpl"}
			{else}
			<h4>{$group->group_name|escape} (MP &laquo;{$group->mp_name|escape}&raquo;) </h4>
			<ul>
				<li>
					<a href="adm_gr_cur/claims.php?mp={$group->mp_id}&gr={$group->group_id}">
						Заявки ({$group->claims})
					</a>             
				</li>
				<li>
					 <!--   <a href="claim_history.php">История заявок</a> -->
				</li>
			</ul> 
			{/if}
		{/foreach}
	</ul>
	{/if}
</td>
<td valign="top" width="50%">
    <h3>Многопроцессорные системы</h3>
    {foreach from=$mplist item=mp}
		<li/>
		<a href="mp.php?id={$mp.mp_id|escape}">{$mp.mp_name|escape}</a>
		({$mp.login|escape})
		<span title="{$mp.help|escape}" style="font-size: 8pt; color: #565656">{$mp.status_descr|escape}</span>
		<ul>
			{if $mp.status=='admin'}
			<li>
				<a href="mp.php?id={$mp.mp_id}&act=claims">Заявки ({$mp.claims})</a>
			</li>
			<li>
				<a href="mp.php?id={$mp.mp_id}&act=key">Ключ доступа</a>
			</li>
			{/if}
			<li>
				<a href="membership/request_user.php?id={$mp.mp_id|escape}">Заявление на доступ</a>
			</li>
		</ul>
    {/foreach}
    
    <a  href="membership/join_mp.php">Зарегистрироваться на машине</a>
    
    <ul>
    <a style="color: #666666; font-size: 80%;" href="register/mp.php">Добавить новую машину</a>
    </ul>

	
    {if isset($admin_menu)}
	{include file="site/admin_menu.tpl"}
	{/if}
</td>
</tr>
</table> **/ ?>
