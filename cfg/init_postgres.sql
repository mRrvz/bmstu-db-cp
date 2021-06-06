DROP DATABASE IF EXISTS lms_dpw;
CREATE DATABASE lms_dpw;
\c lms_dpw;

CREATE TABLE discipline_work_program (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    author VARCHAR(64),
    competency VARCHAR(16) NOT NULL
);

CREATE TABLE learning_outcomes (
    id SERIAL PRIMARY KEY,
    discipline_id INT NOT NULL,
    competency_code VARCHAR(32) NOT NULL,
    formulation VARCHAR(1024) NOT NULL,
    results VARCHAR(2048) NOT NULL,
    forms_and_methods VARCHAR(2048) NOT NULL,
    FOREIGN KEY (discipline_id) REFERENCES discipline_work_program(id)
);

CREATE TABLE educational_program (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

CREATE TABLE discipline_educational_program (
    discipline_id INT NOT NULL,
    educational_program_id VARCHAR(10) NOT NULL,
    FOREIGN KEY (discipline_id) REFERENCES discipline_work_program(id) ON DELETE CASCADE,
    FOREIGN KEY (educational_program_id) REFERENCES educational_program(id) ON DELETE CASCADE
);

CREATE TABLE discipline_scope_semester (
    id SERIAL PRIMARY KEY,
    discipline_id INT NOT NULL,
    semester_number INT NOT NULL,
    credit_units INT NOT NULL,
    total_hours INT NOT NULL,
    lectures_hours INT NOT NULL,
    seminars_hours INT NOT NULL,
    laboratory_work_hours INT NOT NULL,
    independent_work_hours INT NOT NULL,
    certification_type VARCHAR(32) NOT NULL,
    CHECK(certification_type IN('Зачёт', 'Экзамен', 'Зачет')),
    FOREIGN KEY (discipline_id) REFERENCES discipline_work_program(id)
);

CREATE TABLE discipline_module (
    id SERIAL PRIMARY KEY,
    discipline_id INT NOT NULL,
    name VARCHAR(256) NOT NULL,
    semester_number INT NOT NULL,
    lectures_hours INT,
    seminars_hours INT,
    laboratory_work_hours INT,
    independent_work_hours INT,
    min_scores INT NOT NULL,
    max_scores INT NOT NULL,
    competency_codes VARCHAR(1024) NOT NULL,
    FOREIGN KEY (discipline_id) REFERENCES discipline_work_program(id)
);

CREATE TABLE discipline_material (
    id SERIAL PRIMARY KEY,
    discipline_id INT NOT NULL,
    material VARCHAR(1024) NOT NULL,
    FOREIGN KEY (discipline_id) REFERENCES discipline_work_program(id)
);
