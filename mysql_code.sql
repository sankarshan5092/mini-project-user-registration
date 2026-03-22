show databases;
create database curd_nov_2025_mini_project_db;
use curd_nov_2025_mini_project_db;
CREATE TABLE cust_details (
    cust_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    ph_no bigint NOT NULL UNIQUE,
    user_id VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from cust_details;

INSERT INTO cust_details (full_name, address, ph_no, user_id, password) VALUES
('Rajdeep Bhadra', 'Kolkata, West Bengal, India', 9876543210, 'rajdeep01', 'Raj@123');

truncate table cust_details;

select * from cust_details where user_id='SOU@12';

update cust_details
set full_name="rahul bose sharma"
where user_id='rahul@1234';
