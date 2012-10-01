-- MySQL dump 10.13  Distrib 5.5.24, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: aligner
-- ------------------------------------------------------
-- Server version	5.5.24-3-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `algorithms_on_multiprocessor`
--

DROP TABLE IF EXISTS `algorithms_on_multiprocessor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `algorithms_on_multiprocessor` (
  `multiprocessor_id` int(11) NOT NULL,
  `algorithm` varchar(250) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `blast_tasks`
--

DROP TABLE IF EXISTS `blast_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blast_tasks` (
  `task_id` int(10) unsigned NOT NULL,
  `seq_type` enum('nucleotide','protein') NOT NULL DEFAULT 'nucleotide',
  `blast_outp_detail_lvl` tinyint(1) unsigned NOT NULL DEFAULT '8',
  `lower_thrshld` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`task_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hash`
--

DROP TABLE IF EXISTS `hash`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hash` (
  `user_name` varchar(100) NOT NULL,
  `login` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `date_label` date NOT NULL,
  `hash` text,
  PRIMARY KEY (`login`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `multiprocessors`
--

DROP TABLE IF EXISTS `multiprocessors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `multiprocessors` (
  `multiprocessor_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `multiprocessor_name` varchar(25) NOT NULL,
  `num_available_procs` int(10) unsigned NOT NULL,
  `site_url` varchar(250) DEFAULT NULL,
  `path` blob NOT NULL,
  `user_on_it` varchar(20) NOT NULL,
  `host` varchar(250) NOT NULL DEFAULT '',
  `queue_alg` varchar(20) DEFAULT 'simple',
  `state` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`multiprocessor_id`),
  UNIQUE KEY `multiprocessor_name` (`multiprocessor_name`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `passwords`
--

DROP TABLE IF EXISTS `passwords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `passwords` (
  `user_id` int(10) unsigned NOT NULL,
  `password` varchar(200) DEFAULT NULL,
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
  PRIMARY KEY (`task_id`)
) ENGINE=MyISAM AUTO_INCREMENT=90 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-07-30 19:27:56
