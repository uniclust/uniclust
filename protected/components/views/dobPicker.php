<div id="dobPicker">
	<?php echo CHtml::dropDownList($this->dayField, $this->day, $this->getDays(), $this->getDayHtmlOptions()); ?>
	<?php echo CHtml::dropDownList($this->monthField, $this->month, $this->getMonths(), $this->getMonthHtmlOptions()); ?>
	<?php echo CHtml::dropDownList($this->yearField, $this->year, $this->getYears(), $this->getYearHtmlOptions()); ?>
</div>
