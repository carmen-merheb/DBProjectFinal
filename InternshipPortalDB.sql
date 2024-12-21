
-- Create the database
DROP DATABASE IF EXISTS InternshipPortal;
CREATE DATABASE InternshipPortal;

-- Use the created database
USE InternshipPortal;

-- Table: MAJOR
CREATE TABLE MAJOR (
    majorID INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Table: UNIVERSITY
CREATE TABLE UNIVERSITY (
    universityID INT PRIMARY KEY  auto_increment,
    name VARCHAR(255) NOT NULL,
    address TEXT
);

-- Table: UNIVERSITY_MAJOR (junction table)
CREATE TABLE UNIVERSITY_MAJOR (
    universityID INT,
    majorID INT,
    PRIMARY KEY (universityID, majorID),
    FOREIGN KEY (universityID) REFERENCES UNIVERSITY(universityID),
    FOREIGN KEY (majorID) REFERENCES MAJOR(majorID)
);

-- Table: STUDENT
CREATE TABLE STUDENT (
    studentID INT PRIMARY KEY auto_increment,
    fullName VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    birthDate DATE,
    phoneNumber VARCHAR(20),
    resume TEXT,
    universityID INT,
    dateOfEnrollment date,
	FOREIGN KEY (universityID) REFERENCES UNIVERSITY(universityID)
   
);

-- Table: STUDENT_MAJOR (junction table)
CREATE TABLE STUDENT_MAJOR (
    studentID INT,
    majorID INT,
    startDate DATE,
    graduationDate DATE,
    yearOfStudy INT,
    CGPA DECIMAL(4, 2),
    PRIMARY KEY (studentID, majorID),
    FOREIGN KEY (studentID) REFERENCES STUDENT(studentID),
    FOREIGN KEY (majorID) REFERENCES MAJOR(majorID)
);

-- Table: COMPANY
CREATE TABLE COMPANY (
    companyID INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phoneNumber VARCHAR(20)
);



-- Table: DEPARTMENT
CREATE TABLE DEPARTMENT (
    departmentID INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phoneNumber VARCHAR(20),
    companyID INT,
    FOREIGN KEY (companyID) REFERENCES COMPANY(companyID)
);

-- Table: INTERNSHIP
CREATE TABLE INTERNSHIP (
    internshipID INT PRIMARY KEY auto_increment,
    title VARCHAR(255) NOT NULL,
    dateOfPosting DATE,
    deadlineDate DATE,
    description TEXT,
    startDate DATE,
    endDate DATE,
    salary DECIMAL(10, 2),
    isRemote TINYINT(1),
    location VARCHAR(255),
    field VARCHAR(255),
    departmentID INT,
    FOREIGN KEY (departmentID) REFERENCES DEPARTMENT(departmentID)
);

-- Table: APPLICATION
CREATE TABLE APPLICATION (
    applicationID INT PRIMARY KEY auto_increment,
    date DATE NOT NULL,
    status VARCHAR(50),
    internshipID INT,
    studentID INT,
    FOREIGN KEY (internshipID) REFERENCES INTERNSHIP(internshipID),
    FOREIGN KEY (studentID) REFERENCES STUDENT(studentID)
);


-- Table: COMPANYCONTACTS
CREATE TABLE COMPANYCONTACTS (
    contactID INT PRIMARY KEY auto_increment,
    fullName VARCHAR(255) NOT NULL,
    position VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phoneNumber VARCHAR(20),
    companyID INT,
    FOREIGN KEY (companyID) REFERENCES COMPANY(companyID)
);

-- Table: SKILLS
CREATE TABLE SKILLS (
    skillID INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    level VARCHAR(50)
);

CREATE TABLE USER (
    userID INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    studentID INT,
    companyID INT,
    FOREIGN KEY (studentID) REFERENCES STUDENT(studentID),
    FOREIGN KEY (companyID) REFERENCES COMPANY(companyID)
);

-- Table: INTERNSHIP_SKILLS (junction table)
CREATE TABLE INTERNSHIP_SKILLS (
    internshipID INT,
    skillID INT,
    PRIMARY KEY (internshipID, skillID),
    FOREIGN KEY (internshipID) REFERENCES INTERNSHIP(internshipID),
    FOREIGN KEY (skillID) REFERENCES SKILLS(skillID)
);



