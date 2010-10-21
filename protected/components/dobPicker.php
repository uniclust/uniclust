<?php

class dobPicker extends CWidget {
	public $day = 0,
		   $month = 0,
		   $year = 0;

	public $dayField,
		   $monthField,
		   $yearField,
		   $dayClass,
		   $monthClass,
		   $yearClass;
	
	public function run()
	{
		$this->render('dobPicker');
	}

	public function getDays()
	{
		return array_combine(range(1,31), range(1,31));
	}

	public function getMonths()
	{
		return array(
			0  => 'Месяц',
			1  => 'января',
			2  => 'февраля',
			3  => 'марта',
			4  => 'апреля',
			5  => 'мая',
			6  => 'июня',
			7  => 'июля',
			8  => 'августа',
			9  => 'сентября',
			10 => 'октября',
			11 => 'ноября',
			12 => 'декабря'
		);
	}

	public function getYears()
	{
		$years = range(date('Y')-15, 1950);
		return array(0=> 'Год')+array_combine($years, $years);
	}

	public function getDayHtmlOptions()
	{
		$result = array();
		if ($this->dayClass)
		{
			$result['class'] = $this->dayClass;
		}
		return $result;
	}

	public function getMonthHtmlOptions()
	{
		$result = array();
		if ($this->monthClass)
		{
			$result['class'] = $this->monthClass;
		}
		return $result;
	}

	public function getYearHtmloptions()
	{
		$result = array();
		if ($this->yearClass)
		{
			$result['class'] = $this->yearClass;
		}
		return $result;
	}



}
