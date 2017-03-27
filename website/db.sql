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
  -- пользователь для работы на суперкомпьютере
  `user_on_it` varchar(20) NOT NULL,
  `host` varchar(250) NOT NULL,
  `port` int(11) DEFAULT NULL,
  `files_quota` int(11) DEFAULT NULL,
  `description` blob,
  `short_description` text,
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
  `num_procs` int(10) DEFAULT NULL,
  `num_nodes` int(11) DEFAULT NULL,
  `application_id` int(11) NOT NULL,
  `arguments` blob NOT NULL,
  `date_of_creation` date NOT NULL,
  `date_of_finishing` date DEFAULT NULL,
  `comments` text,
  `running_time` datetime DEFAULT NULL,
  `task_status` enum('new','ready','submitted','finished','refused','stopped','running') DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `tokens_used` int(11) DEFAULT NULL,
  `tokenes_allowed` int(11) DEFAULT NULL,
  PRIMARY KEY (`task_id`)
) ENGINE=MyISAM AUTO_INCREMENT=82 DEFAULT CHARSET=utf8;

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

--
-- Table structure for table `operations`
--
DROP TABLE IF EXISTS `operations`;
CREATE TABLE `operations` (
  `operation_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) DEFAULT NULL,
  `oper_type` enum('copyto','copyfrom','remove') DEFAULT NULL,
  `multiprocessor_id` int(11) DEFAULT NULL,
  `status` enum('new','running','finished','canceled','error') DEFAULT NULL,
  `error_message` text DEFAULT NULL,
  PRIMARY KEY (`operation_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
CREATE TABLE `applications` (
  `application_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  `arguments_description` blob NOT NULL,
  `short_description` text,
  PRIMARY KEY (`application_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `apps_on_multiprocessors`
--
DROP TABLE IF EXISTS `apps_on_multiprocessors`;
CREATE TABLE `apps_on_multiprocessors` (
  `application_id` int(11) NOT NULL AUTO_INCREMENT,
  `multiprocessor_id` int(11) NOT NULL,
  `settings` blob NOT NULL,
  PRIMARY KEY (`application_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

--
-- Table structure for table `files`
--
DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
  `file_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `status` enum('ready','processing','error') DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  PRIMARY KEY (`file_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `filecache`
--
DROP TABLE IF EXISTS `filecache`;
CREATE TABLE `filecache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) DEFAULT NULL,
  `multiprocessor_id` int(11) DEFAULT NULL,
  `status` enum('OK','transfer') DEFAULT NULL,
  `read_counter` int(11) DEFAULT NULL,
  `write_counter` int(11) DEFAULT NULL,
  `last_read` datetime DEFAULT NULL,
  `last_write` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `downuploadings`
--
DROP TABLE IF EXISTS `downuploadings`;
CREATE TABLE `downuploadings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL,
  `bytes_downloaded` int(11) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `direction` enum('to','from') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `tasks_files`
--
DROP TABLE IF EXISTS `tasks_files`;
CREATE TABLE `tasks_files` (
  `task_id` int(11) NOT NULL,
  `file_id` int(11) NOT NULL,
  `access_mode` enum('r','w','rw') DEFAULT NULL,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`file_id`,`task_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `clients`
--
DROP TABLE IF EXISTS `clients`;
CREATE TABLE `clients` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `auth_key` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Foreign Keys
--
ALTER TABLE `tasks` ADD FOREIGN KEY (user_id) REFERENCES `users` (`user_id`);
ALTER TABLE `tasks` ADD FOREIGN KEY (multiprocessor_id) REFERENCES `multiprocessors` (`multiprocessor_id`);
ALTER TABLE `tasks` ADD FOREIGN KEY (application_id) REFERENCES `applications` (`application_id`);
ALTER TABLE `users` ADD FOREIGN KEY (user_id) REFERENCES `passwords` (`user_id`);
ALTER TABLE `users` ADD FOREIGN KEY (login) REFERENCES `hash` (`login`);
ALTER TABLE `operations` ADD FOREIGN KEY (file_id) REFERENCES `files` (`file_id`);
ALTER TABLE `operations` ADD FOREIGN KEY (multiprocessor_id) REFERENCES `multiprocessors` (`multiprocessor_id`);
ALTER TABLE `applications` ADD FOREIGN KEY (application_id) REFERENCES `apps_on_multiprocessors` (`application_id`);
ALTER TABLE `apps_on_multiprocessors` ADD FOREIGN KEY (multiprocessor_id) REFERENCES `multiprocessors` (`multiprocessor_id`);
ALTER TABLE `files` ADD FOREIGN KEY (file_id) REFERENCES `tasks_files` (`file_id`);
ALTER TABLE `files` ADD FOREIGN KEY (user_id) REFERENCES `users` (`user_id`);
ALTER TABLE `filecache` ADD FOREIGN KEY (file_id) REFERENCES `files` (`file_id`);
ALTER TABLE `filecache` ADD FOREIGN KEY (operation_id) REFERENCES `operations` (`operation_id`);
ALTER TABLE `filecache` ADD FOREIGN KEY (multiprocessor_id) REFERENCES `multiprocessors` (`multiprocessor_id`);
ALTER TABLE `downuploadings` ADD FOREIGN KEY (file_id) REFERENCES `files` (`file_id`);
ALTER TABLE `downuploadings` ADD FOREIGN KEY (client_id) REFERENCES `clients` (`client_id`);
ALTER TABLE `downuploadings` ADD FOREIGN KEY (user_id) REFERENCES `users` (`user_id`);
ALTER TABLE `tasks_files` ADD FOREIGN KEY (task_id) REFERENCES `tasks` (`task_id`);
ALTER TABLE `clients` ADD FOREIGN KEY (user_id) REFERENCES `users` (`user_id`);
