-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema event_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `event_schema` ;

-- -----------------------------------------------------
-- Schema event_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `event_schema` DEFAULT CHARACTER SET utf8 ;
USE `event_schema` ;

-- -----------------------------------------------------
-- Table `event_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `event_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `event_schema`.`events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `event_schema`.`events` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `event_name` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  `date` DATETIME NULL,
  `description` VARCHAR(255) NULL,
  `member_num` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_events_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_events_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `event_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `event_schema`.`events_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `event_schema`.`events_users` (
  `users_id` INT NOT NULL,
  `events_id` INT NOT NULL,
  INDEX `fk_events_users_users_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_events_users_events1_idx` (`events_id` ASC) VISIBLE,
  CONSTRAINT `fk_events_users_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `event_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_events_users_events1`
    FOREIGN KEY (`events_id`)
    REFERENCES `event_schema`.`events` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
