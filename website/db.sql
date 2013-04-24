--
-- Table structure for table `algorithms_on_multiprocessor`
--
DROP TABLE IF EXISTS `algorithms_on_multiprocessor`;
CREATE TABLE `algorithms_on_multiprocessor` (
  `multiprocessor_id` int(11) NOT NULL,
  `algorithm` varchar(250) NOT NULL,
  `best_num_procs` int(10) unsigned DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


--
-- Table structure for table `hash`
--
DROP TABLE IF EXISTS `hash`;
CREATE TABLE `hash` (
  `user_name` varchar(100) NOT NULL,
  `login` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `date_label` date NOT NULL,
  `hash` text,
  PRIMARY KEY (`login`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


--
-- Table structure for table `multiprocessors`
--
DROP TABLE IF EXISTS `multiprocessors`;
CREATE TABLE `multiprocessors` (
  `multiprocessor_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `multiprocessor_name` varchar(25) NOT NULL,
  `num_available_procs` int(10) unsigned NOT NULL,
  `site_url` varchar(250) DEFAULT NULL,
  `path` blob NOT NULL,
  `user_on_it` varchar(20) NOT NULL,
  `host` varchar(250) NOT NULL DEFAULT '',
  `queue_alg` varchar(20) DEFAULT 'simple',
  PRIMARY KEY (`multiprocessor_id`),
  UNIQUE KEY `multiprocessor_name` (`multiprocessor_name`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


--
-- Table structure for table `passwords`
--
DROP TABLE IF EXISTS `passwords`;
CREATE TABLE `passwords` (
  `user_id` int(10) unsigned NOT NULL,
  `password` varchar(200) DEFAULT NULL,
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


--
-- Table structure for table `tasks`
--
DROP TABLE IF EXISTS `tasks`;
CREATE TABLE `tasks` (
  `task_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `multiprocessor_id` int(10) unsigned NOT NULL,
  `duration_in_minutes` int(10) unsigned NOT NULL,
  `num_procs` int(10) unsigned NOT NULL,
  `algorithm` varchar(250) NOT NULL,
  `date_of_creation` date NOT NULL,
  `date_of_finishing` date DEFAULT NULL,
  `comments` text,
  `priority_run` int(11) DEFAULT '1',
  `priority_max` int(11) DEFAULT '1',
  `running_time` datetime DEFAULT NULL,
  `task_status` enum('new','ready','submitted','finished','refused','stopped','running') DEFAULT NULL,
  `queue_num` int(10) DEFAULT NULL,
  PRIMARY KEY (`task_id`)
) ENGINE=MyISAM AUTO_INCREMENT=82 DEFAULT CHARSET=utf8;


--
-- Table structure for table `blast_tasks`
--
DROP TABLE IF EXISTS `blast_tasks`;
CREATE TABLE `blast_tasks` (
  `task_id` int(10) unsigned NOT NULL,
  `seq_type` enum('nucleotide','protein') NOT NULL DEFAULT 'nucleotide',
  `blast_outp_detail_lvl` tinyint(1) unsigned NOT NULL DEFAULT '8',
  `lower_thrshld` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`task_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


--
-- Table structure for table `users`
--
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(20) NOT NULL DEFAULT '',
  `email` varchar(100) NOT NULL,
  `full_user_name` varchar(250) NOT NULL DEFAULT '',
  `date_of_registration` date NOT NULL,
  `last_login` date NOT NULL,
  `priority_tokens` int(11) DEFAULT '10',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
