drop database lab_management;
CREATE DATABASE IF NOT EXISTS lab_management;
USE lab_management;

-- Таблица услуг
CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    duration INT NOT NULL,
    deviation FLOAT NOT NULL
);

-- Заполнение таблицы услуг
INSERT INTO services (name, cost, code, duration, deviation) VALUES
('Анализ крови', 1500.00, 'A001', 2, 0.05),
('Анализ мочи', 1200.00, 'A002', 1, 0.03),
('Биохимический анализ', 2500.00, 'A003', 3, 0.07);

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    passport_series VARCHAR(20) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    insurance_number VARCHAR(50) NOT NULL,
    insurance_type VARCHAR(50) NOT NULL,
    insurance_company VARCHAR(100) NOT NULL,
    role ENUM('lab_worker', 'researcher', 'accountant', 'admin') NOT NULL
);

-- Заполнение таблицы пользователей
INSERT INTO users (login, password, full_name, birth_date, passport_series, phone, email, insurance_number, insurance_type, insurance_company, role) VALUES
('lab1', 'pass123', 'Иван Иванов', '1985-07-10', '4509123456', '89031234567', 'ivanov@mail.com', '1234567890', 'ОМС', 'Росгосстрах', 'lab_worker'),
('research1', 'pass234', 'Петр Петров', '1990-03-22', '4510123457', '89032345678', 'petrov@mail.com', '0987654321', 'ДМС', 'Согаз', 'researcher'),
('account1', 'pass345', 'Анна Смирнова', '1982-11-05', '4521123458', '89033456789', 'smirnova@mail.com', '1122334455', 'ОМС', 'АльфаСтрахование', 'accountant'),
('admin1', 'adminpass', 'Сергей Васильев', '1978-05-30', '4532123459', '89034567890', 'vasilyev@mail.com', '6677889900', 'ДМС', 'Ресо', 'admin');

-- Таблица страховых компаний
CREATE TABLE IF NOT EXISTS insurance_companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    address TEXT NOT NULL,
    inn VARCHAR(20) UNIQUE NOT NULL,
    bank_account VARCHAR(50) UNIQUE NOT NULL,
    bic VARCHAR(20) NOT NULL
);

-- Заполнение таблицы страховых компаний
INSERT INTO insurance_companies (name, address, inn, bank_account, bic) VALUES
('Росгосстрах', 'Москва, ул. Ленина, 1', '7701234567', '40702810900000000001', '044525225'),
('Согаз', 'Санкт-Петербург, Невский проспект, 10', '7801234568', '40702810900000000002', '044525226'),
('АльфаСтрахование', 'Москва, ул. Тверская, 5', '7701234569', '40702810900000000003', '044525227'),
('Ресо', 'Казань, ул. Баумана, 15', '1601234570', '40702810900000000004', '044525228');

-- Таблица заказов
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'in_progress', 'completed') NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES users(id)
);

-- Заполнение таблицы заказов
INSERT INTO orders (patient_id, status) VALUES
(1, 'pending'),
(2, 'in_progress'),
(3, 'completed');

-- Таблица оказанных услуг
CREATE TABLE IF NOT EXISTS provided_services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    service_id INT NOT NULL,
    performed_by INT,
    analyzer VARCHAR(100),
    performed_at DATETIME DEFAULT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (service_id) REFERENCES services(id),
    FOREIGN KEY (performed_by) REFERENCES users(id)
);

-- Заполнение таблицы оказанных услуг
INSERT INTO provided_services (order_id, service_id, performed_by, analyzer, performed_at) VALUES
(1, 1, 2, 'Анализатор A1', '2025-02-25 10:00:00'),
(2, 2, 2, 'Анализатор B2', '2025-02-25 11:00:00');
















-- Добавление таблицы истории входов
CREATE TABLE IF NOT EXISTS login_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Обновление таблицы пользователей (добавление последнего входа)
ALTER TABLE users ADD COLUMN last_login DATETIME DEFAULT NULL;

-- Добавление триггера для обновления времени последнего входа
DELIMITER $$
CREATE TRIGGER update_last_login
AFTER INSERT ON login_history
FOR EACH ROW
BEGIN
    IF NEW.success = TRUE THEN
        UPDATE users SET last_login = NEW.login_time WHERE id = NEW.user_id;
    END IF;
END$$
DELIMITER ;
CREATE TABLE IF NOT EXISTS user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_start DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_end DATETIME DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
-- Добавление таблицы блокировок пользователей
CREATE TABLE IF NOT EXISTS user_blocking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    blocked_until DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
