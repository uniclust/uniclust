--
-- База данных: `uniclust`
--

-- --------------------------------------------------------

--
-- Структура таблицы `claims`
--

CREATE TABLE IF NOT EXISTS `claims` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `type` enum('curator','head','mp','admin') NOT NULL,
  `subtype` varchar(50) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `target_id` int(10) unsigned NOT NULL,
  `is_primary` varchar(100) NOT NULL,
  `param1` varchar(100) DEFAULT NULL,
  `param2` varchar(100) DEFAULT NULL,
  `data` text,
  `considered` enum('no','satisfied','unsatisfied') NOT NULL DEFAULT 'no',
  `considered_by` int(10) unsigned NOT NULL DEFAULT '0',
  `consideration_date` datetime NOT NULL,
  `reason` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `email_confirmations`
--

CREATE TABLE IF NOT EXISTS `email_confirmations` (
  `user_id` int(10) unsigned NOT NULL,
  `email` varchar(250) NOT NULL,
  `hash` varchar(32) NOT NULL,
  PRIMARY KEY (`user_id`,`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `groups`
--

CREATE TABLE IF NOT EXISTS `groups` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int(10) unsigned NOT NULL,
  `group_name` varchar(100) NOT NULL,
  `os_group_name` varchar(20) NOT NULL,
  `group_description` text,
  `status` enum('new','registered','locked','deleted') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `os_group_name` (`os_group_name`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `group_multiprocessor_relations`
--

CREATE TABLE IF NOT EXISTS `group_multiprocessor_relations` (
  `group_id` int(10) unsigned NOT NULL,
  `multiprocessor_id` int(10) unsigned NOT NULL,
  `status` enum('preliminary','new','registered','pre_locked','locked','deleted') NOT NULL DEFAULT 'preliminary',
  `curator_id` int(11) NOT NULL DEFAULT '0',
  `request_tpl` text,
  PRIMARY KEY (`group_id`,`multiprocessor_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `hash`
--

CREATE TABLE IF NOT EXISTS `hash` (
  `user_name` varchar(100) NOT NULL,
  `login` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `date_label` date NOT NULL,
  `hash` text,
  PRIMARY KEY (`login`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `multiprocessors`
--

CREATE TABLE IF NOT EXISTS `multiprocessors` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `organization_id` int(10) unsigned NOT NULL,
  `public_access` enum('yes','no') NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `support_email` varchar(100) NOT NULL,
  `dns_addresses_list` varchar(250) DEFAULT NULL,
  `description` text NOT NULL,
  `status` enum('new','registered') NOT NULL DEFAULT 'new',
  `access_key` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `organizations`
--

CREATE TABLE IF NOT EXISTS `organizations` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `russian_short_name` varchar(30) NOT NULL,
  `english_short_name` varchar(30) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `organization_description` text,
  `phone` varchar(100) DEFAULT NULL,
  `address` text NOT NULL,
  `head` text NOT NULL,
  `status` enum('registered','locked','new') NOT NULL DEFAULT 'new',
  PRIMARY KEY (`id`),
  UNIQUE KEY `russian_short_name` (`russian_short_name`),
  UNIQUE KEY `english_short_name` (`english_short_name`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `password_reminds`
--

CREATE TABLE IF NOT EXISTS `password_reminds` (
  `user_id` int(10) unsigned NOT NULL,
  `register` enum('yes','no') NOT NULL DEFAULT 'no',
  `hash` varchar(32) NOT NULL,
  UNIQUE KEY `hash` (`hash`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(20) NOT NULL,
  `password` varchar(200) NOT NULL,
  `full_user_name` varchar(250) NOT NULL,
  `latin_user_name` varchar(250) NOT NULL,
  `phones` varchar(250) DEFAULT NULL,
  `interests` text,
  `other_information` text,
  `user_status` enum('new','registered','locked','deleted') NOT NULL DEFAULT 'new',
  `date_of_registration` int(10) unsigned NOT NULL,
  `primary_email` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `user_emails`
--

CREATE TABLE IF NOT EXISTS `user_emails` (
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `email` varchar(250) NOT NULL,
  PRIMARY KEY (`user_id`,`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `user_group_relations`
--

CREATE TABLE IF NOT EXISTS `user_group_relations` (
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `group_id` int(10) unsigned NOT NULL DEFAULT '0',
  `is_primary` enum('yes','no') DEFAULT 'no',
  `status` enum('new','registered','head') DEFAULT 'registered',
  PRIMARY KEY (`user_id`,`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `user_multiprocessor_relations`
--

CREATE TABLE IF NOT EXISTS `user_multiprocessor_relations` (
  `user_id` int(10) unsigned NOT NULL,
  `multiprocessor_id` int(10) unsigned NOT NULL,
  `primary_group` int(10) unsigned NOT NULL DEFAULT '0',
  `user_status` enum('registered','locked','new','pre_locked','deleted','unlocked','admin') NOT NULL DEFAULT 'new',
  `login_on_machine` varchar(20) NOT NULL,
  `uid_on_machine` int(10) unsigned DEFAULT NULL,
  `registration_date` date DEFAULT NULL,
  `request_tpl` text NOT NULL,
  PRIMARY KEY (`user_id`,`multiprocessor_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `user_organization_relations`
--

CREATE TABLE IF NOT EXISTS `user_organization_relations` (
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `organization_id` int(10) unsigned NOT NULL DEFAULT '0',
  `is_primary` enum('yes','no') DEFAULT 'no',
  `position` varchar(100) DEFAULT NULL,
  `status` enum('registered','chpos') NOT NULL DEFAULT 'registered',
  PRIMARY KEY (`user_id`,`organization_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

