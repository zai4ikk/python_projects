-- MySQL Script generated by MySQL Workbench
-- Fri Jul  5 17:10:00 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema buh
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema buh
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `buh` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `buh` ;

-- -----------------------------------------------------
-- Table `buh`.`positions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buh`.`positions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `p_name` VARCHAR(40) NULL DEFAULT NULL,
  `p_salary` DECIMAL(8,2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `buh`.`operation_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buh`.`operation_type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `op_name` VARCHAR(40) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `buh`.`calculations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buh`.`calculations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `c_datetime` DATETIME NULL DEFAULT NULL,
  `c_summ` DECIMAL(8,2) NULL DEFAULT NULL,
  `id_pos` INT NULL DEFAULT NULL,
  `id_operation` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `id_pos` (`id_pos` ASC) VISIBLE,
  INDEX `id_operation` (`id_operation` ASC) VISIBLE,
  CONSTRAINT `calculations_ibfk_1`
    FOREIGN KEY (`id_pos`)
    REFERENCES `buh`.`positions` (`id`),
  CONSTRAINT `calculations_ibfk_2`
    FOREIGN KEY (`id_operation`)
    REFERENCES `buh`.`operation_type` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `buh`.`donations_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buh`.`donations_type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `d_name` VARCHAR(40) NULL DEFAULT NULL,
  `size` DECIMAL(8,2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `buh`.`position_donations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buh`.`position_donations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_positions` INT NULL DEFAULT NULL,
  `id_donat` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `id_positions` (`id_positions` ASC) VISIBLE,
  INDEX `id_donat` (`id_donat` ASC) VISIBLE,
  CONSTRAINT `position_donations_ibfk_1`
    FOREIGN KEY (`id_positions`)
    REFERENCES `buh`.`positions` (`id`),
  CONSTRAINT `position_donations_ibfk_2`
    FOREIGN KEY (`id_donat`)
    REFERENCES `buh`.`donations_type` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

USE `buh` ;

-- -----------------------------------------------------
-- function calculate_amount
-- -----------------------------------------------------

DELIMITER $$
USE `buh`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `calculate_amount`(id_positions INT, id_donations_type INT, id_operation_type INT) RETURNS decimal(10,2)
    READS SQL DATA
BEGIN
    DECLARE total DECIMAL(10, 2);
    DECLARE salary DECIMAL(10, 2);
    SELECT p_salary INTO salary FROM positions WHERE id = id_positions;
    
    IF id_operation_type = 1 THEN
        SELECT salary - (SUM(size) * salary / 100) INTO total
        FROM position_donations
        JOIN donations_type ON position_donations.id_donat = donations_type.id
        WHERE id_positions = id_positions AND id_operation_type = id_operation_type AND id_donat = id_donations_type;
    ELSE
        SELECT SUM(size) * salary / 100 INTO total
        FROM position_donations
        JOIN donations_type ON position_donations.id_donat = donations_type.id
        WHERE id_positions = id_positions AND id_operation_type = id_operation_type AND id_donat = id_donations_type;
    END IF;
    RETURN total;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure calculate_amount_procedure
-- -----------------------------------------------------

DELIMITER $$
USE `buh`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `calculate_amount_procedure`(
    IN in_position_id INT,
    IN in_donations_type_id INT,
    IN in_operation_type_id INT,
    OUT out_total DECIMAL(10,2)
)
BEGIN
    DECLARE salary DECIMAL(10,2);
    
    SELECT p_salary INTO salary FROM positions WHERE id = in_position_id;

    IF in_operation_type_id = 1 THEN
        SELECT salary - (SUM(size) * salary / 100) INTO out_total
        FROM position_donations
        JOIN donations_type ON position_donations.id_donat = donations_type.id
        WHERE id_positions = in_position_id AND id_donat = in_donations_type_id;
    ELSE
        SELECT SUM(size) * salary / 100 INTO out_total
        FROM position_donations
        JOIN donations_type ON position_donations.id_donat = donations_type.id
        WHERE id_positions = in_position_id AND id_donat = in_donations_type_id;
    END IF;
    
    INSERT INTO calculations (c_datetime, c_summ, id_pos, id_operation) 
    VALUES (NOW(), out_total, in_position_id, in_operation_type_id);
    
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
USE `buh`;

DELIMITER $$
USE `buh`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `buh`.`monthly_insert_check_trigger`
BEFORE INSERT ON `buh`.`calculations`
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM calculations 
        WHERE id_pos = NEW.id_pos 
        AND id_operation = NEW.id_operation 
        AND MONTH(c_datetime) = MONTH(NOW())
        AND YEAR(c_datetime) = YEAR(NOW())
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Нельзя вставить данные более одного раза в месяц для данного сотрудника и типа операции';
    END IF;
END$$


DELIMITER ;
