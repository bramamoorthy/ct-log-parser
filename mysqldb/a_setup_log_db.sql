DROP TABLE IF EXISTS `access_log_details`;

CREATE TABLE `access_log_details` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ip` varchar(150) DEFAULT NULL,
  `device_brand` varchar(100) DEFAULT NULL,
  `device_model` varchar(64) DEFAULT NULL,
  `os_family` varchar(100) DEFAULT NULL,
  `browser` varchar(100) DEFAULT NULL,
  `latitude` decimal(18,5) DEFAULT NULL,
  `longitude` decimal(18,5) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;