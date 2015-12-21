-- MySQL Script generated by MySQL Workbench
-- 12/20/15 15:19:05
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema webclock
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema webclock
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `webclock` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `webclock` ;

-- -----------------------------------------------------
-- Table `webclock`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webclock`.`User` (
  `user_id` VARCHAR(45) NOT NULL COMMENT '',
  `user_passwd` VARCHAR(45) NOT NULL COMMENT '',
  `user_email` VARCHAR(45) NOT NULL COMMENT '',
  PRIMARY KEY (`user_id`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `webclock`.`Course`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webclock`.`Course` (
  `course_id` VARCHAR(45) NOT NULL COMMENT '',
  `course_name` VARCHAR(45) NULL COMMENT '',
  `user_id` VARCHAR(45) NOT NULL COMMENT '',
  `course_enable` INT NULL COMMENT '',
  `notice_enable` INT NULL COMMENT '',
  `homework_enable` INT NULL COMMENT '',
  `file_enable` INT NULL COMMENT '',
  `course_url` VARCHAR(500) NULL COMMENT '',
  PRIMARY KEY (`course_id`)  COMMENT '',
  INDEX `fk_Course_User_idx` (`user_id` ASC)  COMMENT '',
  CONSTRAINT `fk_Course_User`
    FOREIGN KEY (`user_id`)
    REFERENCES `webclock`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `webclock`.`Homework`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webclock`.`Homework` (
  `course_id` VARCHAR(45) NOT NULL COMMENT '',
  `send_state` INT NULL COMMENT '',
  `alarm_state` INT NULL COMMENT '',
  `url` VARCHAR(500) NULL COMMENT '',
  `homework_name` VARCHAR(45) NULL COMMENT '',
  `homework_id` VARCHAR(45) NOT NULL COMMENT '',
  `deadline` DATETIME NULL COMMENT '',
  PRIMARY KEY (`homework_id`)  COMMENT '',
  INDEX `fk_CourseHomework_Course1_idx` (`course_id` ASC)  COMMENT '',
  CONSTRAINT `fk_CourseHomework_Course1`
    FOREIGN KEY (`course_id`)
    REFERENCES `webclock`.`Course` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `webclock`.`File`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webclock`.`File` (
  `file_id` VARCHAR(45) NOT NULL COMMENT '',
  `course_id` VARCHAR(45) NOT NULL COMMENT '',
  `send_state` INT NULL COMMENT '',
  PRIMARY KEY (`file_id`, `course_id`)  COMMENT '',
  INDEX `fk_CourseFile_Course1_idx` (`course_id` ASC)  COMMENT '',
  CONSTRAINT `fk_CourseFile_Course1`
    FOREIGN KEY (`course_id`)
    REFERENCES `webclock`.`Course` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;