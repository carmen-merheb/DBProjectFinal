-- Insert data into MAJOR
INSERT INTO MAJOR (majorID, name, description)
VALUES 
    (1, 'Computer Science', 'Study of computation and computer systems'),
    (2, 'Mechanical Engineering', 'Study of machines and mechanical systems'),
    (3, 'Electrical Engineering', 'Study of electrical systems and circuits'),
    (4, 'Civil Engineering', 'Study of construction and infrastructure'),
    (5, 'Business Administration', 'Study of managing businesses'),
    (6, 'Psychology', 'Study of the human mind and behavior'),
    (7, 'Physics', 'Study of matter and energy'),
    (8, 'Mathematics', 'Study of numbers and abstract concepts'),
    (9, 'Chemical Engineering', 'Study of chemical processes'),
    (10, 'Data Science', 'Study of data analysis and machine learning');

-- Insert data into UNIVERSITY
INSERT INTO UNIVERSITY (universityID, name, address)
VALUES 
    (1, 'MIT', '77 Massachusetts Ave, Cambridge, MA'),
    (2, 'Stanford University', '450 Serra Mall, Stanford, CA'),
    (3, 'Harvard University', 'Cambridge, MA'),
    (4, 'UC Berkeley', 'Berkeley, CA'),
    (5, 'University of Oxford', 'Oxford, UK'),
    (6, 'University of Cambridge', 'Cambridge, UK'),
    (7, 'ETH Zurich', 'Zurich, Switzerland'),
    (8, 'Caltech', '1200 E California Blvd, Pasadena, CA'),
    (9, 'Carnegie Mellon University', '5000 Forbes Ave, Pittsburgh, PA'),
    (10, 'Imperial College London', 'London, UK');

-- Insert data into UNIVERSITY_MAJOR
INSERT INTO UNIVERSITY_MAJOR (universityID, majorID)
VALUES 
    (1, 1), (1, 2), (2, 3), (2, 4), (3, 5),
    (4, 6), (5, 7), (6, 8), (7, 9), (8, 10);

-- Insert data into STUDENT

INSERT INTO STUDENT (studentID, fullName, email, birthDate, phoneNumber, resume, universityID, dateOfEnrollment)
VALUES 
    (1, 'Alice Smith', 'alice.smith@example.com', '2001-09-01', '1234567890', 'Alice_resume.pdf', 10, '2020-09-01'),
    (2, 'Bob Johnson', 'bob.johnson@example.com', '2001-09-01', '1234567891', 'Bob_resume.pdf', 2, '2020-09-01'),
    (3, 'Charlie Brown', 'charlie.brown@example.com', '2001-09-01', '1234567892', 'Charlie_resume.pdf', 3, '2020-09-01'),
    (4, 'Diana Ross', 'diana.ross@example.com', '2001-09-01', '1234567893', 'Diana_resume.pdf', 4, '2020-09-01'),
    (5, 'Eve Davis', 'eve.davis@example.com', '2001-09-01', '1234567894', 'Eve_resume.pdf', 5, '2020-09-01'),
    (6, 'Frank Miller', 'frank.miller@example.com', '2001-09-01', '1234567895', 'Frank_resume.pdf', 6, '2020-09-01'),
    (7, 'Grace Lee', 'grace.lee@example.com', '2001-09-01', '1234567896', 'Grace_resume.pdf', 7, '2020-09-01'),
    (8, 'Hank Green', 'hank.green@example.com', '2001-09-01', '1234567897', 'Hank_resume.pdf', 8, '2020-09-01'),
    (9, 'Ivy Wilson', 'ivy.wilson@example.com', '2001-09-01', '1234567898', 'Ivy_resume.pdf', 9, '2020-09-01'),
    (10, 'Jack Black', 'jack.black@example.com', '2001-09-01', '1234567899', 'Jack_resume.pdf', 1, '2020-09-01');



-- Insert data into STUDENT_MAJOR
INSERT INTO STUDENT_MAJOR (studentID, majorID, startDate, graduationDate, yearOfStudy, CGPA)
VALUES 
    (1, 1, '2018-09-01', '2022-06-01', 4, 3.80),
    (2, 2, '2017-09-01', '2021-06-01', 4, 3.75),
    (3, 3, '2019-09-01', '2023-06-01', 3, 3.90),
    (4, 4, '2018-09-01', '2022-06-01', 4, 3.70),
    (5, 5, '2016-09-01', '2020-06-01', 4, 3.85),
    (6, 6, '2015-09-01', '2019-06-01', 4, 3.95),
    (7, 7, '2019-09-01', '2023-06-01', 3, 3.65),
    (8, 8, '2017-09-01', '2021-06-01', 4, 3.78),
    (9, 9, '2018-09-01', '2022-06-01', 4, 3.82),
    (10, 10, '2016-09-01', '2020-06-01', 4, 3.88);

-- Insert data into COMPANY
INSERT INTO COMPANY (companyID, name, industry, email, phoneNumber)
VALUES 
    (1, 'Tech Solutions', 'Technology', 'info@techsolutions.com', '9876543210'),
    (2, 'BuildIt Corp', 'Construction', 'info@buildit.com', '9876543211'),
    (3, 'HealthCare Inc.', 'Healthcare', 'info@healthcare.com', '9876543212'),
    (4, 'Green Energy', 'Energy', 'info@greenenergy.com', '9876543213'),
    (5, 'EdTech Academy', 'Education', 'info@edtechacademy.com', '9876543214'),
    (6, 'FinancePro', 'Finance', 'info@financepro.com', '9876543215'),
    (7, 'AutoDrive', 'Automobile', 'info@autodrive.com', '9876543216'),
    (8, 'RetailGiant', 'Retail', 'info@retailgiant.com', '9876543217'),
    (9, 'Foodies', 'Food & Beverage', 'info@foodies.com', '9876543218'),
    (10, 'TravelEase', 'Travel', 'info@travelease.com', '9876543219');

-- Insert data into DEPARTMENT
INSERT INTO DEPARTMENT (departmentID, name, address, phoneNumber, companyID)
VALUES 
    (1, 'R&D', '123 Tech Ave, Silicon Valley', '1112223330', 1),
    (2, 'Construction Management', '456 Build St, NY', '1112223331', 2),
    (3, 'Clinical Research', '789 Health Blvd, LA', '1112223332', 3),
    (4, 'Sustainable Energy', '321 Green Ln, TX', '1112223333', 4),
    (5, 'EdTech Innovations', '654 Academy Rd, SF', '1112223334', 5),
    (6, 'Wealth Management', '987 Finance Dr, Chicago', '1112223335', 6),
    (7, 'Autonomous Vehicles', '159 Auto St, Detroit', '1112223336', 7),
    (8, 'Retail Operations', '753 Retail Rd, Seattle', '1112223337', 8),
    (9, 'Product Development', '852 Food Ave, Miami', '1112223338', 9),
    (10, 'Travel Support', '951 Travel Blvd, Boston', '1112223339', 10);
    
-- Insert data into the SKILLS table
INSERT INTO SKILLS (skillID, name, level) VALUES
    (1, 'Python', 'Intermediate'),
    (2, 'Java', 'Advanced'),
    (3, 'SQL', 'Beginner'),
    (4, 'Machine Learning', 'Advanced'),
    (5, 'Data Analysis', 'Intermediate'),
    (6, 'Project Management', 'Intermediate'),
    (7, 'Communication', 'Advanced'),
    (8, 'Team Leadership', 'Advanced'),
    (9, 'Cybersecurity', 'Beginner'),
    (10, 'Cloud Computing', 'Intermediate');

-- Insert data into the INTERNSHIP table
INSERT INTO INTERNSHIP (internshipID, title, dateOfPosting, deadlineDate, description, startDate, endDate, salary, isRemote, location, field, departmentID) VALUES
    (1, 'Software Engineering Intern', '2024-01-01', '2024-02-01', 'Work on backend systems.', '2024-06-01', '2024-12-01', 1500.00, 1, 'New York', 'Software Development', 1),
    (2, 'Data Analyst Intern', '2024-01-05', '2024-02-15', 'Analyze company data.', '2024-06-01', '2024-09-01', 1200.00, 0, 'San Francisco', 'Data Analysis', 2),
    (3, 'Cybersecurity Intern', '2024-01-10', '2024-02-20', 'Ensure system security.', '2024-07-01', '2024-12-01', 1600.00, 0, 'Austin', 'Cybersecurity', 3),
    (4, 'Cloud Solutions Intern', '2024-01-15', '2024-03-01', 'Work on cloud migration.', '2024-06-01', '2024-12-01', 1400.00, 1, 'Seattle', 'Cloud Computing', 4),
    (5, 'AI Research Intern', '2024-01-20', '2024-03-10', 'Develop AI models.', '2024-06-01', '2024-11-01', 2000.00, 0, 'Boston', 'Artificial Intelligence', 5),
    (6, 'Marketing Analyst Intern', '2024-02-01', '2024-03-15', 'Analyze market trends.', '2024-07-01', '2024-10-01', 1100.00, 1, 'Chicago', 'Marketing', 6),
    (7, 'Embedded Systems Intern', '2024-01-25', '2024-03-05', 'Develop IoT devices.', '2024-05-01', '2024-11-01', 1300.00, 0, 'San Diego', 'Embedded Systems', 7),
    (8, 'DevOps Intern', '2024-02-10', '2024-03-20', 'Automate deployments.', '2024-05-15', '2024-10-15', 1450.00, 1, 'Denver', 'DevOps', 8),
    (9, 'HR Intern', '2024-02-15', '2024-03-25', 'Support HR activities.', '2024-06-01', '2024-09-01', 1000.00, 0, 'Atlanta', 'Human Resources', 9),
    (10, 'Blockchain Intern', '2024-02-20', '2024-03-30', 'Research blockchain.', '2024-07-01', '2024-12-01', 1700.00, 0, 'Miami', 'Blockchain', 10);

-- Insert data into the APPLICATION table
INSERT INTO APPLICATION (applicationID, date, status, internshipID, studentID) VALUES
    (1, '2024-03-01', 'Pending', 1, 1),
    (2, '2024-03-05', 'Approved', 2, 2),
    (3, '2024-03-10', 'Rejected', 3, 3),
    (4, '2024-03-15', 'Pending', 4, 4),
    (5, '2024-03-20', 'Approved', 5, 5),
    (6, '2024-03-25', 'Rejected', 6, 6),
    (7, '2024-03-30', 'Pending', 7, 7),
    (8, '2024-04-01', 'Approved', 8, 8),
    (9, '2024-04-05', 'Rejected', 9, 9),
    (10, '2024-04-10', 'Pending', 10, 10);

-- Insert data into the COMPANYCONTACTS table
INSERT INTO COMPANYCONTACTS (contactID, fullName, position, email, phoneNumber, companyID) VALUES
    (1, 'Alice Johnson', 'HR Manager', 'alice.johnson@company1.com', '555-1001', 1),
    (2, 'Bob Smith', 'Tech Lead', 'bob.smith@company2.com', '555-1002', 2),
    (3, 'Catherine Brown', 'Data Scientist', 'catherine.brown@company3.com', '555-1003', 3),
    (4, 'David White', 'Cloud Engineer', 'david.white@company4.com', '555-1004', 4),
    (5, 'Emma Green', 'AI Specialist', 'emma.green@company5.com', '555-1005', 5),
    (6, 'Frank Harris', 'Marketing Head', 'frank.harris@company6.com', '555-1006', 6),
    (7, 'Grace Lee', 'IoT Engineer', 'grace.lee@company7.com', '555-1007', 7),
    (8, 'Henry Scott', 'DevOps Manager', 'henry.scott@company8.com', '555-1008', 8),
    (9, 'Isabella Martinez', 'HR Executive', 'isabella.martinez@company9.com', '555-1009', 9),
    (10, 'Jack Taylor', 'Blockchain Developer', 'jack.taylor@company10.com', '555-1010', 10);

-- Insert data into the INTERNSHIP_SKILLS table
INSERT INTO INTERNSHIP_SKILLS (internshipID, skillID) VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (2, 5),
    (3, 9),
    (4, 10),
    (5, 4),
    (6, 7),
    (7, 1),
    (8, 6),
    (9, 8),
    (10, 4);

-- Insert data into the USER table
INSERT INTO USER (userID, email, password, studentID, companyID) VALUES
    (1, 'student1@example.com', 'password1', 1, NULL),
    (2, 'student2@example.com', 'password2', 2, NULL),
    (3, 'student3@example.com', 'password3', 3, NULL),
    (4, 'student4@example.com', 'password4', 4, NULL),
    (5, 'student5@example.com', 'password5', 5, NULL),
    (6, 'company1@example.com', 'password6', NULL, 1),
    (7, 'company2@example.com', 'password7', NULL, 2),
    (8, 'company3@example.com', 'password8', NULL, 3),
    (9, 'company4@example.com', 'password9', NULL, 4),
    (10, 'company5@example.com', 'password10', NULL, 5);

