CREATE DATABASE machine_test_db;

USE machine_test_db;

CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpass123';

GRANT ALL PRIVILEGES ON machine_test_db.* TO 'testuser'@'localhost';

FLUSH PRIVILEGES;


