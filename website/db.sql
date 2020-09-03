--
-- SQL script for creating database for uniclust
--

--
-- All tables are deleted in order reverse to creation.
-- We need this because dependencies by foreign keys.
--
DROP TABLE IF EXISTS `tasks_files`;
DROP TABLE IF EXISTS `downuploadings`;
DROP TABLE IF EXISTS `clients`;
DROP TABLE IF EXISTS `filecache`;
DROP TABLE IF EXISTS `apps_on_multiprocessors`;
DROP TABLE IF EXISTS `operations`;
DROP TABLE IF EXISTS `files`;
DROP TABLE IF EXISTS `tasks`;
DROP TABLE IF EXISTS `applications`;
DROP TABLE IF EXISTS `passwords`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `multiprocessors`;
DROP TABLE IF EXISTS `hash`;


--
-- Table structure for table `hash`
--
CREATE TABLE `hash` (
  `user_name` varchar(100) NOT NULL,
  `login` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `date_label` date NOT NULL,
  `hash` text,
  PRIMARY KEY (`login`)
) DEFAULT CHARSET=utf8;

--
-- Table structure for table `multiprocessors`
--
CREATE TABLE `multiprocessors` (
  `multiprocessor_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `multiprocessor_name` varchar(100) NOT NULL,
  `num_available_procs` int(11) unsigned NOT NULL,
  `site_url` varchar(250) DEFAULT NULL,
  `path` blob NOT NULL,
  -- пользователь для работы на суперкомпьютере
  `user_on_it` varchar(20) NOT NULL,
  `host` varchar(250) NOT NULL,
  `port` int(6) unsigned DEFAULT NULL,
  `files_quota` int(11) unsigned DEFAULT NULL,
  `description` blob,
  `short_description` text,
  PRIMARY KEY (`multiprocessor_id`),
  UNIQUE KEY `multiprocessor_name` (`multiprocessor_name`)
) DEFAULT CHARSET=utf8;

--
-- Table structure for table `users`
--
CREATE TABLE `users` (
  `user_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(20) NOT NULL DEFAULT '',
  `email` varchar(100) NOT NULL,
  `full_user_name` varchar(250) NOT NULL DEFAULT '',
  `date_of_registration` date DEFAULT NULL,
  `last_login` date DEFAULT NULL,
  `priority_tokens` int(11) DEFAULT '10',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `login` (`login`)
) DEFAULT CHARSET=utf8;

--
-- Table structure for table `passwords`
--
CREATE TABLE `passwords` (
  `user_id` int(11) unsigned NOT NULL,
  `password` varchar(200) DEFAULT NULL,
  UNIQUE KEY `user_id` (`user_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
) DEFAULT CHARSET=utf8;

--
-- Table structure for table `applications`
--
CREATE TABLE `applications` (
  `application_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `arguments_description` blob NOT NULL,
  `short_description` text,
  PRIMARY KEY (`application_id`)
)  DEFAULT CHARSET=utf8;


--
-- Table structure for table `tasks`
--
CREATE TABLE `tasks` (
  `task_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned NOT NULL,
  `multiprocessor_id` int(11) unsigned NOT NULL,
  `duration_in_minutes` int(11) unsigned NOT NULL,
  `num_procs` int(11) unsigned DEFAULT NULL,
  `num_nodes` int(11) unsigned DEFAULT NULL,
  `application_id` int(11) unsigned DEFAULT NULL,
  `arguments` blob NOT NULL,
  `date_of_creation` date DEFAULT NULL,
  `date_of_finishing` date DEFAULT NULL,
  `comments` text,
  `running_time` datetime DEFAULT NULL,
  `task_status` enum('new','ready','submitted','finished','refused','stopped','running') DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `tokens_used` int(11) DEFAULT NULL,
  `tokenes_allowed` int(11) DEFAULT NULL,
  PRIMARY KEY (`task_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`),
  FOREIGN KEY (`multiprocessor_id`) REFERENCES `multiprocessors`(`multiprocessor_id`),
  FOREIGN KEY (`application_id`) REFERENCES `applications` (`application_id`)
) DEFAULT CHARSET=utf8;

--
-- Table structure for table `files`
--
CREATE TABLE `files` (
  `file_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `status` enum('ready','processing','error') DEFAULT NULL,
  `user_id` int(11) unsigned DEFAULT NULL,
  `size` bigint unsigned DEFAULT NULL,
  -- Number of usage events for this file
  `num_of_reads` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`file_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
) DEFAULT CHARSET=utf8;

--
-- Table structure for table `operations`
--
CREATE TABLE `operations` (
  `operation_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `file_id` int(11) unsigned DEFAULT NULL,
  `oper_type` enum('copyto','copyfrom','remove') DEFAULT NULL,
  `multiprocessor_id` int(11) unsigned DEFAULT NULL,
  `status` enum('new','running','finished','canceled','error') DEFAULT NULL,
  `error_message` text DEFAULT NULL,
  PRIMARY KEY (`operation_id`),
  FOREIGN KEY (`file_id`) REFERENCES `files` (`file_id`),
  FOREIGN KEY (`multiprocessor_id`) REFERENCES `multiprocessors` (`multiprocessor_id`)  
)  DEFAULT CHARSET=utf8;

--
-- Table structure for table `apps_on_multiprocessors`
--
CREATE TABLE `apps_on_multiprocessors` (
  `application_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `multiprocessor_id` int(11) unsigned NOT NULL,
  `settings` blob NOT NULL,
  PRIMARY KEY (`application_id`,`multiprocessor_id`),
  FOREIGN KEY (`application_id`) REFERENCES `applications` (`application_id`),
  FOREIGN KEY (`multiprocessor_id`) REFERENCES `multiprocessors` (`multiprocessor_id`)  
) DEFAULT CHARSET=utf8;


--
-- Table structure for table `filecache`
--
CREATE TABLE `filecache` (
  `filecache_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `file_id` int(11) unsigned DEFAULT NULL,
  `multiprocessor_id` int(11) unsigned  DEFAULT NULL,
  `status` enum('OK','transfer') DEFAULT NULL,
  `read_counter` int(11)  unsigned DEFAULT NULL,
  `write_counter` int(11) unsigned DEFAULT NULL,
  `last_read` datetime DEFAULT NULL,
  `last_write` datetime DEFAULT NULL,
  PRIMARY KEY (`filecache_id`),
  FOREIGN KEY (`file_id`) REFERENCES `files` (`file_id`),
  FOREIGN KEY (`multiprocessor_id`) REFERENCES `multiprocessors` (`multiprocessor_id`)
) DEFAULT CHARSET=utf8;

--
-- Table structure for table `clients`
--
CREATE TABLE `clients` (
  `client_id` int(11) unsigned  NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned NOT NULL,
  `auth_key` blob DEFAULT NULL,
  PRIMARY KEY (`client_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
)  DEFAULT CHARSET=utf8;


--
-- Table structure for table `downuploadings`
--
CREATE TABLE `downuploadings` (
  `downuploadings_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `file_id` int(11) unsigned NOT NULL,
  `bytes_downloaded` bigint unsigned DEFAULT NULL,
  `client_id` int(11) unsigned DEFAULT NULL,
  `user_id` int(11) unsigned DEFAULT NULL,
  `direction` enum('to','from') DEFAULT NULL,
  PRIMARY KEY (`downuploadings_id`),
  FOREIGN KEY (`file_id`) REFERENCES `files` (`file_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`)
)  DEFAULT CHARSET=utf8;

--
-- Table structure for table `tasks_files`
--
CREATE TABLE `tasks_files` (
  `task_id` int(11) unsigned NOT NULL,
  `file_id` int(11) unsigned NOT NULL,
  `access_mode` enum('r','w','rw') DEFAULT NULL,
  `status` int(10) NOT NULL,
  PRIMARY KEY (`file_id`,`task_id`),
  FOREIGN KEY (`file_id`) REFERENCES `files` (`file_id`),
  FOREIGN KEY (`task_id`) REFERENCES `tasks` (`task_id`)  
)  DEFAULT CHARSET=utf8;


