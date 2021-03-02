CREATE DATABASE discord_covid19;

USE discord_covid19;

DROP TABLE IF EXISTS `covid19`;
CREATE TABLE `covid19` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `countryID` int(6) NOT NULL,
  `confirmedCount` int(10) unsigned NOT NULL,
  `curedCount` int(10) unsigned NOT NULL,
  `deadCount` int(10) unsigned NOT NULL,
  `timeRecorded` bigint(16) unsigned DEFAULT NULL,
  `active_cases` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) unsigned DEFAULT NULL,
  `neet_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;