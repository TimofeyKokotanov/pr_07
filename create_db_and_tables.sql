CREATE DATABASE medical_db;

\c medical_db;

CREATE TABLE doctors (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    SPECIALIZATION VARCHAR(100) NOT NULL,
    HOSPITAL VARCHAR(100) NOT NULL
);

CREATE TABLE appointments (
    ID SERIAL PRIMARY KEY,
    DOCTOR_ID INT REFERENCES doctors(ID),
    DATE DATE NOT NULL
);

CREATE TABLE patients (
    ID SERIAL PRIMARY KEY,
    DOCTOR_ID INT REFERENCES doctors(ID),
    AGE INT NOT NULL,
    NAME VARCHAR(100)
);

INSERT INTO doctors (NAME, SPECIALIZATION, HOSPITAL) VALUES
('Dr. Smith', 'Neurologist', 'City Hospital'),
('Dr. Johnson', 'Cardiologist', 'General Hospital'),
('Dr. Lee', 'Neurologist', 'Central Clinic');

INSERT INTO appointments (DOCTOR_ID, DATE) VALUES
(1, '2023-10-01'),
(1, '2023-10-02'),
(2, '2023-10-03');

INSERT INTO patients (DOCTOR_ID, AGE, NAME) VALUES
(1, 35, 'John Doe'),
(1, 45, 'Jane Smith'),
(2, 50, 'Alice Brown');