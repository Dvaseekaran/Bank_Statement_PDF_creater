-- Create Database
CREATE DATABASE IF NOT EXISTS ocbc_bank;
USE ocbc_bank;

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    aadhar_number VARCHAR(12) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(15) UNIQUE,
    password_hash VARCHAR(255), -- store hashed passwords
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accounts Table
CREATE TABLE IF NOT EXISTS Accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    account_number VARCHAR(20) UNIQUE,
    account_type VARCHAR(50),
    balance DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Transactions Table
CREATE TABLE IF NOT EXISTS Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    transaction_type VARCHAR(50), -- e.g., 'deposit', 'withdrawal', 'transfer'
    amount DECIMAL(15, 2),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255),
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);

-- Login Sessions Table
CREATE TABLE IF NOT EXISTS Login_Sessions (
    session_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Beneficiaries Table
CREATE TABLE IF NOT EXISTS Beneficiaries (
    beneficiary_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    beneficiary_account_number VARCHAR(20),
    beneficiary_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Rewards Table (Optional, for credit card points etc.)
CREATE TABLE IF NOT EXISTS Rewards (
    reward_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    points INT DEFAULT 0,
    reward_description VARCHAR(255),
    earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
-- Insert sample users
INSERT INTO Users (aadhar_number, full_name, email, phone_number, password_hash) VALUES
('123456789012', 'Alice Kumar', 'alice@example.com', '9123456789', 'hashed_password1'),
('234567890123', 'Bob Singh', 'bob@example.com', '9234567890', 'hashed_password2');

-- Insert sample accounts
INSERT INTO Accounts (user_id, account_number, account_type, balance) VALUES
(1, 'OCBC10001', 'Savings', 5000.00),
(2, 'OCBC10002', 'Current', 10000.00);

-- Insert sample transactions
INSERT INTO Transactions (account_id, transaction_type, amount, description) VALUES
(1, 'deposit', 2000.00, 'Initial deposit'),
(2, 'withdrawal', 1500.00, 'ATM Withdrawal'),
(1, 'transfer', 500.00, 'Transfer to Beneficiary');

-- Insert sample beneficiaries
INSERT INTO Beneficiaries (user_id, beneficiary_account_number, beneficiary_name) VALUES
(1, 'OCBC10002', 'Bob Singh');
