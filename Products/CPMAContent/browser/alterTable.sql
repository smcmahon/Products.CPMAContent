ALTER TABLE `profiles` ADD `address3` TEXT NOT NULL ,
ADD `city3` TINYTEXT NOT NULL ,
ADD `state3` TINYTEXT NOT NULL ,
ADD `zip3` MEDIUMINT( 5 ) NOT NULL ,
ADD `phone3` TINYTEXT NOT NULL ,
ADD `hours3` TEXT NOT NULL;

ALTER TABLE `members` ADD `company` TINYTEXT NOT NULL ;
