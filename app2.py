import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error
import os
from werkzeug.utils import secure_filename
import re
from flask import send_file

# Create a Flask app instance
app = Flask(__name__)

app.config['SECRET_KEY'] = 'root'

# File upload settings
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define the database connection parameters
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Sensea@2004&2024",
        database="InternshipPortal"
    )

# Route for student sign-up form
@app.route('/signup/student', methods=['GET', 'POST'])
def signup_student():
    if request.method == 'POST':
        # Extract data from the form
        full_name = request.form['fullName']
        email = request.form['email']
        phone_number = request.form['phoneNumber']
        birth_date = request.form['birthDate']  # 
        university_name = request.form['university']
        date_of_enrollment = request.form['dateOfEnrollment']
        major_name = request.form['major']
        password = request.form['password']

        # Hash the password
        hashed_password = generate_password_hash(password)
        
        

        # Create database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if the email exists in the USER table
        if email_exists(cursor, email):
            flash('This email is already in use. Please use a different one or <a href="' + url_for('login') + '">login</a>.')

            return redirect(url_for('signup_student'))


        # Validate password strength
        if not is_password_strong(password):
            flash('Password is too weak. It must be at least 8 characters long, include 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character.', 'error')
            return redirect(url_for('signup_student'))

        # Fetch universityID by university name
        cursor.execute("SELECT universityID FROM UNIVERSITY WHERE name = %s", (university_name,))
        university_id = cursor.fetchone()

        if university_id is None:
            return "University not found", 404

        university_id = university_id[0]

        # Fetch majorID by major name
        cursor.execute("SELECT majorID FROM MAJOR WHERE name = %s", (major_name,))
        major_id = cursor.fetchone()

        if major_id is None:
            return "Major not found", 404

        major_id = major_id[0]

        # Insert student into STUDENT table
        cursor.execute("""
            INSERT INTO STUDENT (fullName, email, phoneNumber, birthDate, universityID, dateOfEnrollment)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (full_name, email, phone_number, birth_date, university_id, date_of_enrollment))

        # Commit the transaction
        conn.commit()

        # Get the studentID of the newly inserted student (auto-incremented)
        cursor.execute("SELECT LAST_INSERT_ID()")
        student_id = cursor.fetchone()[0]

        # Insert into STUDENT_MAJOR table to link student with major
        cursor.execute("""
            INSERT INTO STUDENT_MAJOR (studentID, majorID)
            VALUES (%s, %s)
        """, (student_id, major_id))
        
         # Insert into USER table (mapping email, password, and studentID)
        cursor.execute("""
            INSERT INTO USER (email, password, studentID)
            VALUES (%s, %s, %s)
        """, (email, hashed_password, student_id))

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return redirect(url_for('student_welcome'))

    # If GET request, show the sign-up form with dynamic university and major lists
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch universities
    cursor.execute("SELECT name FROM UNIVERSITY")
    universities = cursor.fetchall()

    # Fetch majors
    cursor.execute("SELECT name FROM MAJOR")
    majors = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('register_student.html', universities=universities, majors=majors)

@app.route('/signup/company', methods=['GET', 'POST'])
def signup_company():
    if request.method == 'POST':
        # Extract data from the form
        company_name = request.form['companyName']
        email = request.form['email']
        phone_number = request.form['phoneNumber']
        industry = request.form['industry']
        password = request.form['password']

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Check if the email exists in the USER table
            if email_exists(cursor, email):
                flash('This email is already in use. Please use a different one or <a href="' + url_for('login') + '">login</a>.')
                return render_template('register_company.html', company=None)

            # Validate password strength
            if not is_password_strong(password):
                flash('Password is too weak. It must be at least 8 characters long, include 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character.', 'error')
                return render_template('register_company.html', company=None)

            # Insert the company into the COMPANY table
            cursor.execute("""
                INSERT INTO COMPANY (name, email, phoneNumber, industry)
                VALUES (%s, %s, %s, %s)
            """, (company_name, email, phone_number, industry))

            # Commit the transaction
            conn.commit()

            # Get the companyID of the newly inserted company (auto-incremented)
            cursor.execute("SELECT LAST_INSERT_ID()")
            company_id = cursor.fetchone()[0]

            # Insert a new user into the USER table
            cursor.execute("""
                INSERT INTO USER (email, password, companyID)
                VALUES (%s, %s, %s)
            """, (email, hashed_password, company_id))

            # Commit the transaction and close the connection
            conn.commit()
            return redirect(url_for('company_welcome'))

        except Exception as e:
            conn.rollback()
            flash(f"An error occurred: {str(e)}", "error")

        finally:
            cursor.close()
            conn.close()

    # If GET request, show the company sign-up form
    return render_template('register_company.html', company=None)



# Route for the homepage (Welcome page)
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Route for the Sign Up page (where user chooses role)
@app.route('/signup')
def signup():
    return render_template('role.html')

@app.route('/tobeimplemented')
def tobeimplemented():
    return render_template('tobeimplemented.html')


from flask import session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the user exists in the USER table
        cursor.execute("SELECT * FROM USER WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session.clear()  # Clear any existing session
            session['userID'] = user['userID']  # Store user ID for both types
            if user.get('studentID'):
                session['studentID'] = user['studentID']  # Add studentID
                return redirect(url_for('student_welcome'))
            elif user.get('companyID'):
                session['companyID'] = user['companyID']  # Add companyID
                return redirect(url_for('company_welcome'))
        else:
            flash('Invalid email or password.', 'error')

        cursor.close()
        conn.close()

    return render_template('login.html')


@app.route('/student_welcome')
def student_welcome():
    if 'studentID' not in session:
        flash("You must be logged in to access this page.", "error")
        return redirect(url_for('login'))

    student_id = session['studentID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT fullName FROM STUDENT WHERE studentID = %s", (student_id,))
        student = cursor.fetchone()
    finally:
        cursor.close()
        db_connection.close()

    return render_template('student_welcome.html', student=student)


@app.route('/company_welcome')
def company_welcome():
    # Ensure the user is logged in as a company
    if 'companyID' not in session:
        flash("You must be logged in as a company to access this page.", "error")
        return redirect(url_for('login'))

    company_id = session['companyID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Fetch company information
        cursor.execute("SELECT name FROM COMPANY WHERE companyID = %s", (company_id,))
        company = cursor.fetchone()

        if not company:
            flash("Company not found.", "error")
            return redirect(url_for('login'))

    finally:
        cursor.close()
        db_connection.close()

    # Render the company welcome page
    return render_template('company_welcome.html', company=company)

from datetime import date

@app.route('/company_dashboard')
def company_dashboard():
    # Ensure the user is logged in as a company
    if 'companyID' not in session:
        flash("You must be logged in as a company to access the dashboard.", "error")
        return redirect(url_for('login'))

    company_id = session['companyID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Fetch company name
        cursor.execute("SELECT name FROM COMPANY WHERE companyID = %s", (company_id,))
        company_name = cursor.fetchone().get('name')

        # Total internships posted by the company
        cursor.execute("""
            SELECT COUNT(*) AS total_internships 
            FROM INTERNSHIP 
            WHERE departmentID IN (
                SELECT departmentID FROM DEPARTMENT WHERE companyID = %s
            )
        """, (company_id,))
        total_internships = cursor.fetchone().get('total_internships', 0)

        # Total applications received for company's internships
        cursor.execute("""
            SELECT COUNT(*) AS total_applications 
            FROM APPLICATION 
            WHERE internshipID IN (
                SELECT internshipID FROM INTERNSHIP WHERE departmentID IN (
                    SELECT departmentID FROM DEPARTMENT WHERE companyID = %s
                )
            )
        """, (company_id,))
        total_applications = cursor.fetchone().get('total_applications', 0)

        # Active internships
        cursor.execute("""
            SELECT COUNT(*) AS active_internships 
            FROM INTERNSHIP 
            WHERE departmentID IN (
                SELECT departmentID FROM DEPARTMENT WHERE companyID = %s
            ) AND endDate >= CURDATE()
        """, (company_id,))
        active_internships = cursor.fetchone().get('active_internships', 0)

        # Recent internships (last 5 posted)
        cursor.execute("""
            SELECT title, startDate 
            FROM INTERNSHIP 
            WHERE departmentID IN (
                SELECT departmentID FROM DEPARTMENT WHERE companyID = %s
            )
            ORDER BY startDate DESC
            LIMIT 5
        """, (company_id,))
        recent_internships = cursor.fetchall()

        # All internships with application counts
        cursor.execute("""
            SELECT i.internshipID, i.title, i.startDate, i.endDate,
                   (SELECT COUNT(*) FROM APPLICATION WHERE APPLICATION.internshipID = i.internshipID) AS applications
            FROM INTERNSHIP i
            WHERE i.departmentID IN (
                SELECT departmentID FROM DEPARTMENT WHERE companyID = %s
            )
        """, (company_id,))
        internships = cursor.fetchall()

    finally:
        cursor.close()
        db_connection.close()

    # Render the template
    return render_template(
        'company_dashboard.html',
        company_name=company_name,
        total_internships=total_internships,
        total_applications=total_applications,
        active_internships=active_internships,
        recent_internships=recent_internships,
        internships=internships,
        date = date
    )


@app.route('/edit_internship/<int:internship_id>', methods=['GET', 'POST'])
def edit_internship(internship_id):
    # Ensure the user is logged in as a company
    if 'companyID' not in session:
        flash("You must be logged in as a company to edit an internship.", "error")
        return redirect(url_for('login'))

    company_id = session['companyID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Verify the internship belongs to the logged-in company
        cursor.execute("""
            SELECT i.*, d.companyID
            FROM INTERNSHIP i
            INNER JOIN DEPARTMENT d ON i.departmentID = d.departmentID
            WHERE i.internshipID = %s AND d.companyID = %s
        """, (internship_id, company_id))
        internship = cursor.fetchone()

        if not internship:
            flash("You do not have permission to edit this internship.", "error")
            return redirect(url_for('company_dashboard'))

        if request.method == 'POST':
            # Get form data
            title = request.form['title']
            deadline_date = request.form['deadlineDate']
            description = request.form['description']
            start_date = request.form['startDate']
            end_date = request.form['endDate']
            salary = request.form['salary']
            location = request.form['location']
            field = request.form['field']
            is_remote = 1 if 'isRemote' in request.form else 0  # Checkbox handling

            # Update the internship record
            cursor.execute("""
                UPDATE INTERNSHIP
                SET title = %s, deadlineDate = %s, description = %s, startDate = %s, endDate = %s, 
                    salary = %s, location = %s, field = %s, isRemote = %s
                WHERE internshipID = %s
            """, (title, deadline_date, description, start_date, end_date, salary, location, field, is_remote, internship_id))
            db_connection.commit()

            flash("Internship updated successfully!", "success")
            return redirect(url_for('company_dashboard'))

        # Render the edit form with existing data
        return render_template('edit_internship.html', internship=internship)

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        db_connection.rollback()
        return redirect(url_for('company_dashboard'))

    finally:
        cursor.close()
        db_connection.close()


@app.route('/delete_internship/<int:internship_id>', methods=['POST'])
def delete_internship(internship_id):
    # Ensure the user is logged in as a company
    if 'companyID' not in session:
        flash("You must be logged in as a company to delete an internship.", "error")
        return redirect(url_for('login'))

    company_id = session['companyID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    try:
        # Ensure the internship belongs to the logged-in company
        cursor.execute("""
            SELECT i.internshipID 
            FROM INTERNSHIP i
            INNER JOIN DEPARTMENT d ON i.departmentID = d.departmentID
            WHERE i.internshipID = %s AND d.companyID = %s
        """, (internship_id, company_id))
        internship = cursor.fetchone()

        if not internship:
            flash("You do not have permission to delete this internship.", "error")
            return redirect(url_for('company_dashboard'))

        # Delete applications associated with the internship
        cursor.execute("""
            DELETE FROM APPLICATION WHERE internshipID = %s
        """, (internship_id,))

        # Delete skills mapping in INTERNSHIP_SKILLS
        cursor.execute("""
            DELETE FROM INTERNSHIP_SKILLS WHERE internshipID = %s
        """, (internship_id,))

        # Delete the internship itself
        cursor.execute("""
            DELETE FROM INTERNSHIP WHERE internshipID = %s
        """, (internship_id,))

        db_connection.commit()
        flash("Internship successfully deleted.", "success")
    except Exception as e:
        db_connection.rollback()
        flash(f"An error occurred: {str(e)}", "error")
    finally:
        cursor.close()
        db_connection.close()

    return redirect(url_for('company_dashboard'))


from datetime import datetime

@app.route('/post_internship', methods=['GET', 'POST'])
def post_internship():
    if 'companyID' not in session:
        flash("You must be logged in as a company to post an internship.", "error")
        return redirect(url_for('login'))

    company_id = session['companyID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            # Department information
            department_name = request.form['departmentName']
            address = request.form['address']
            phone_number = request.form['phoneNumber']

            # Check if department exists
            cursor.execute("""
                SELECT departmentID FROM DEPARTMENT
                WHERE name = %s AND companyID = %s
            """, (department_name, company_id))
            existing_department = cursor.fetchone()

            if existing_department:
                department_id = existing_department['departmentID']
            else:
                cursor.execute("""
                    INSERT INTO DEPARTMENT (name, address, phoneNumber, companyID)
                    VALUES (%s, %s, %s, %s)
                """, (department_name, address, phone_number, company_id))
                db_connection.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")
                department_id = cursor.fetchone()['LAST_INSERT_ID()']

            # Internship information
            title = request.form['title']
            deadline_date = request.form['deadlineDate']
            description = request.form['description']
            start_date = request.form['startDate']
            end_date = request.form['endDate']
            salary = request.form['salary']
            location = request.form['location']
            field = request.form['field']
            is_remote = 1 if 'isRemote' in request.form else 0  # Checkbox handling
            date_of_posting = datetime.now().strftime('%Y-%m-%d')

            # Insert into INTERNSHIP table
            cursor.execute("""
                INSERT INTO INTERNSHIP (title, dateOfPosting, deadlineDate, description, startDate, endDate, salary, location, field, departmentID, isRemote)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (title, date_of_posting, deadline_date, description, start_date, end_date, salary, location, field, department_id, is_remote))
            db_connection.commit()

            # Internship skills
            cursor.execute("SELECT LAST_INSERT_ID()")
            internship_id = cursor.fetchone()['LAST_INSERT_ID()']
            skill_names = request.form.getlist('skillName')
            skill_levels = request.form.getlist('skillLevel')

            for skill_name, skill_level in zip(skill_names, skill_levels):
                cursor.execute("""
                    SELECT skillID FROM SKILLS WHERE name = %s AND level = %s
                """, (skill_name, skill_level))
                skill = cursor.fetchone()
                if skill:
                    skill_id = skill['skillID']
                    cursor.execute("""
                        INSERT INTO INTERNSHIP_SKILLS (internshipID, skillID)
                        VALUES (%s, %s)
                    """, (internship_id, skill_id))
                    db_connection.commit()

            flash("Internship successfully posted!", "success")
            return redirect(url_for('company_dashboard'))

        # Render form with available skills
        cursor.execute("SELECT DISTINCT name FROM SKILLS")
        available_skills = cursor.fetchall()
        return render_template('post_internship.html', available_skills=available_skills)

    except Exception as e:
        db_connection.rollback()
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('company_dashboard'))

    finally:
        cursor.close()
        db_connection.close()



@app.route('/company_edit', methods=['GET', 'POST'])
def company_edit():
    # Ensure the user is logged in as a company
    if 'companyID' not in session:
        flash("You must be logged in as a company to access this page.", "error")
        return redirect(url_for('login'))

    company_id = session['companyID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        if request.method == 'GET':
            # Fetch current company data
            cursor.execute("SELECT * FROM COMPANY WHERE companyID = %s", (company_id,))
            company = cursor.fetchone()

            if not company:
                flash("Company not found.", "error")
                return redirect(url_for('company_dashboard'))

            # Render the company_edit.html template
            return render_template('company_edit.html', company=company)

        elif request.method == 'POST':
            # Get form data
            name = request.form['name']
            industry = request.form['industry']
            phone_number = request.form['phoneNumber']

            # Update company table
            cursor.execute("""
                UPDATE COMPANY
                SET name = %s, industry = %s, phoneNumber = %s
                WHERE companyID = %s
            """, (name, industry, phone_number, company_id))

            # Commit changes and redirect to the company dashboard
            db_connection.commit()
            flash("Your company information has been successfully updated.", "success")
            return redirect(url_for('company_dashboard'))

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('company_dashboard'))

    finally:
        cursor.close()
        db_connection.close()

    # Fallback response in case of unexpected behavior
    flash("Invalid request method.", "error")
    return redirect(url_for('company_dashboard'))



@app.route('/add_company_contact', methods=['GET', 'POST'])
def add_company_contact():
    # Ensure the user is logged in as a company
    if 'companyID' not in session:
        flash("You must be logged in as a company to add a contact.", "error")
        return redirect(url_for('login'))

    company_id = session['companyID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    try:
        if request.method == 'POST':
            # Extract data from the form
            full_name = request.form['fullName']
            position = request.form['position']
            email = request.form['email']
            phone_number = request.form['phoneNumber']

            # Insert the new contact into the COMPANYCONTACTS table
            cursor.execute("""
                INSERT INTO COMPANYCONTACTS (fullName, position, email, phoneNumber, companyID)
                VALUES (%s, %s, %s, %s, %s)
            """, (full_name, position, email, phone_number, company_id))

            # Commit the transaction
            db_connection.commit()

            flash("Company contact successfully added!", "success")
            return redirect(url_for('company_dashboard'))

        # For GET requests, render the add_company_contact.html form
        return render_template('add_company_contact.html')

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        db_connection.rollback()
        return redirect(url_for('company_dashboard'))

    finally:
        cursor.close()
        db_connection.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads', 'resumes')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/student_edit', methods=['GET', 'POST'])
def student_edit():
    # Ensure the user is logged in as a student
    if 'studentID' not in session:
        flash("You must be logged in to access this page.", "error")
        return redirect(url_for('login'))

    student_id = session['studentID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        if request.method == 'GET':
            # Fetch current student data
            cursor.execute("SELECT * FROM STUDENT WHERE studentID = %s", (student_id,))
            student = cursor.fetchone()

            if not student:
                flash("Student not found.", "error")
                return redirect(url_for('student_dashboard'))

            # Fetch university and major options
            cursor.execute("SELECT universityID, name FROM UNIVERSITY")
            universities = cursor.fetchall()

            cursor.execute("SELECT majorID, name FROM MAJOR")
            majors = cursor.fetchall()

            # Fetch major details
            cursor.execute("""
                SELECT sm.majorID, sm.startDate, sm.graduationDate, sm.yearOfStudy, sm.CGPA, m.name AS majorName
                FROM STUDENT_MAJOR sm
                JOIN MAJOR m ON sm.majorID = m.majorID
                WHERE sm.studentID = %s
            """, (student_id,))
            major_info = cursor.fetchone()

            # Render the student_edit.html template
            return render_template(
                'student_edit.html',
                student=student,
                universities=universities,
                majors=majors,
                major_info=major_info
            )

        elif request.method == 'POST':
            # Fetch current student data to get the existing resume file name
            cursor.execute("SELECT * FROM STUDENT WHERE studentID = %s", (student_id,))
            student = cursor.fetchone()

            if not student:
                flash("Student not found.", "error")
                return redirect(url_for('student_dashboard'))

            # Handle form submission
            full_name = request.form['fullName']
            phone_number = request.form.get('phoneNumber')
            birth_date = request.form['birthDate']
            university_id = request.form['universityID']
            enrollment_date = request.form['dateOfEnrollment'] or None

            # Handle resume upload
            resume = request.files.get('resume')
            resume_filename = student.get('resume')  # Default to the existing resume

            if resume and allowed_file(resume.filename):
                resume_filename = secure_filename(resume.filename)
                resume_path = os.path.join(UPLOAD_FOLDER, resume_filename)
                resume.save(resume_path)
            elif resume and not allowed_file(resume.filename):
                flash("Invalid file type. Only PDF, DOC, and DOCX are allowed.", "error")
                return redirect(url_for('student_edit'))

            # Update student table
            cursor.execute("""
                UPDATE STUDENT
                SET fullName = %s, phoneNumber = %s, birthDate = %s, universityID = %s, resume = %s, dateOfEnrollment = %s
                WHERE studentID = %s
            """, (full_name, phone_number, birth_date, university_id, resume_filename, enrollment_date, student_id))

            # Update or insert into STUDENT_MAJOR table
            major_id = request.form.get('majorID') or None
            start_date = request.form.get('startDate') or None
            graduation_date = request.form.get('graduationDate') or None
            year_of_study = request.form.get('yearOfStudy') or None
            cgpa = request.form.get('CGPA') or None

            cursor.execute("""
                INSERT INTO STUDENT_MAJOR (studentID, majorID, startDate, graduationDate, yearOfStudy, CGPA)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    startDate = VALUES(startDate),
                    graduationDate = VALUES(graduationDate),
                    yearOfStudy = VALUES(yearOfStudy),
                    CGPA = VALUES(CGPA)
            """, (student_id, major_id, start_date, graduation_date, year_of_study, cgpa))

            # Commit changes and redirect to the dashboard
            db_connection.commit()
            flash("Your profile has been successfully updated.", "success")
            return redirect(url_for('student_dashboard'))

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('student_dashboard'))

    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

    # Return a fallback response in case no path is matched
    flash("Invalid request method.", "error")
    return redirect(url_for('student_dashboard'))

@app.route('/internship_listings')
def internship_listings():
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Fetch all internships with associated company and department details
        cursor.execute("""
            SELECT i.internshipID, i.title, i.startDate, i.endDate, i.location, 
                   i.salary, i.isRemote, d.name AS departmentName, c.name AS companyName
            FROM INTERNSHIP i
            INNER JOIN DEPARTMENT d ON i.departmentID = d.departmentID
            INNER JOIN COMPANY c ON d.companyID = c.companyID
            ORDER BY i.startDate DESC
        """)
        internships = cursor.fetchall()

    finally:
        cursor.close()
        db_connection.close()

    # Render the internship listings page
    return render_template('internship_listings.html', internships=internships)

@app.route('/internship_details/<int:internship_id>')
def internship_details(internship_id):
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Fetch internship details
        cursor.execute("""
            SELECT i.*, d.name AS departmentName, c.name AS companyName, c.industry AS companyIndustry
            FROM INTERNSHIP i
            INNER JOIN DEPARTMENT d ON i.departmentID = d.departmentID
            INNER JOIN COMPANY c ON d.companyID = c.companyID
            WHERE i.internshipID = %s
        """, (internship_id,))
        internship = cursor.fetchone()

        if not internship:
            flash("Internship not found.", "error")
            return redirect(url_for('internship_listings'))

        # Fetch company contacts
        cursor.execute("""
            SELECT fullName, position, email, phoneNumber
            FROM COMPANYCONTACTS
            WHERE companyID = (
                SELECT companyID FROM DEPARTMENT WHERE departmentID = %s
            )
        """, (internship['departmentID'],))
        contacts = cursor.fetchall()

    finally:
        cursor.close()
        db_connection.close()

    return render_template('internship_details.html', internship=internship, contacts=contacts)


@app.route('/student_dashboard')
def student_dashboard():
    # Check if student is logged in
    if 'studentID' not in session:
        flash("You must be logged in as a student to access the dashboard.", "error")
        return redirect(url_for('login'))

    student_id = session['studentID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Fetch student information
        cursor.execute("""
            SELECT s.fullName, s.email, s.phoneNumber, s.birthDate, s.dateOfEnrollment, u.name AS universityName
            FROM STUDENT s
            JOIN UNIVERSITY u ON s.universityID = u.universityID
            WHERE s.studentID = %s
        """, (student_id,))
        student = cursor.fetchone()

        # Fetch major information
        cursor.execute("""
            SELECT sm.startDate, sm.graduationDate, sm.yearOfStudy, sm.CGPA, m.name AS majorName
            FROM STUDENT_MAJOR sm
            JOIN MAJOR m ON sm.majorID = m.majorID
            WHERE sm.studentID = %s
        """, (student_id,))
        major_info = cursor.fetchone()

        # Fetch internship applications
        cursor.execute("""
            SELECT i.title, i.startDate, i.endDate, i.location, a.status
            FROM APPLICATION a
            JOIN INTERNSHIP i ON a.internshipID = i.internshipID
            WHERE a.studentID = %s
        """, (student_id,))
        internships = cursor.fetchall()

    except Exception as e:
        flash("An error occurred while fetching your data: " + str(e), "error")
        return redirect(url_for('welcome'))

    finally:
        cursor.close()
        db_connection.close()

    # Render the student dashboard
    return render_template(
        'student_dashboard.html',
        student=student,
        major_info=major_info,
        internships=internships
    )

    
@app.route('/apply_for_internship/<int:internship_id>', methods=['GET', 'POST'])
def apply_for_internship(internship_id):
    # Ensure the user is logged in as a student
    if 'studentID' not in session:
        flash("You must be logged in as a student to apply for an internship.", "error")
        return redirect(url_for('login'))

    student_id = session['studentID']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            # Check if the student has already applied
            cursor.execute("""
                SELECT * FROM APPLICATION WHERE internshipID = %s AND studentID = %s
            """, (internship_id, student_id))
            application = cursor.fetchone()

            if application:
                flash("You have already applied for this internship.", "warning")
                return redirect(url_for('internship_details', internship_id=internship_id))

            # Add a new application
            cursor.execute("""
                INSERT INTO APPLICATION (date, status, internshipID, studentID)
                VALUES (CURDATE(), 'Pending', %s, %s)
            """, (internship_id, student_id))
            db_connection.commit()

            flash("Your application has been submitted successfully!", "success")
            return redirect(url_for('student_dashboard'))

        # Fetch internship details
        cursor.execute("""
            SELECT title, internshipID FROM INTERNSHIP WHERE internshipID = %s
        """, (internship_id,))
        internship = cursor.fetchone()

        if not internship:
            flash("Internship not found.", "error")
            return redirect(url_for('internship_listings'))

        # Fetch student's current information
        cursor.execute("""
            SELECT fullName, phoneNumber, birthDate, email, dateOfEnrollment
            FROM STUDENT
            WHERE studentID = %s
        """, (student_id,))
        student = cursor.fetchone()

        return render_template(
            'apply_for_internship.html',
            internship=internship,
            student=student
        )

    except Exception as e:
        db_connection.rollback()
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('internship_listings'))

    finally:
        cursor.close()
        db_connection.close()

@app.route('/view_applications/<int:internship_id>', methods=['GET', 'POST'])
def view_applications(internship_id):
    # Ensure the user is logged in as a company
    if 'companyID' not in session:
        flash("You must be logged in as a company to view applications.", "error")
        return redirect(url_for('login'))

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            application_id = request.form.get('application_id')
            action = request.form.get('action')

            if action == 'accept_single':
                # Accept this application and reject all others for the same internship
                cursor.execute("""
                    SELECT internshipID FROM APPLICATION WHERE applicationID = %s
                """, (application_id,))
                internship = cursor.fetchone()
                if internship:
                    internship_id = internship['internshipID']
                    # Reject all other applications for the same internship
                    cursor.execute("""
                        UPDATE APPLICATION
                        SET status = 'Rejected'
                        WHERE internshipID = %s AND applicationID != %s
                    """, (internship_id, application_id))
                    # Accept the current application
                    cursor.execute("""
                        UPDATE APPLICATION
                        SET status = 'Accepted'
                        WHERE applicationID = %s
                    """, (application_id,))
                    db_connection.commit()
                    flash("This application has been accepted and others have been rejected.", "success")
            elif action == 'accept_multiple':
                # Accept this application only
                cursor.execute("""
                    UPDATE APPLICATION
                    SET status = 'Accepted'
                    WHERE applicationID = %s
                """, (application_id,))
                db_connection.commit()
                flash("This application has been accepted.", "success")
            elif action == 'reject':
                # Reject this application
                cursor.execute("""
                    UPDATE APPLICATION
                    SET status = 'Rejected'
                    WHERE applicationID = %s
                """, (application_id,))
                db_connection.commit()
                flash("This application has been rejected.", "success")
            return redirect(url_for('view_applications', internship_id=internship_id))

        # Fetch internship details
        cursor.execute("""
            SELECT i.title, i.startDate, i.endDate, d.name AS departmentName, c.name AS companyName
            FROM INTERNSHIP i
            INNER JOIN DEPARTMENT d ON i.departmentID = d.departmentID
            INNER JOIN COMPANY c ON d.companyID = c.companyID
            WHERE i.internshipID = %s
        """, (internship_id,))
        internship = cursor.fetchone()

        if not internship:
            flash("Internship not found.", "error")
            return redirect(url_for('company_dashboard'))

        # Fetch applications for the internship
        cursor.execute("""
            SELECT a.applicationID, a.date, a.status, s.fullName, s.email, s.phoneNumber
            FROM APPLICATION a
            INNER JOIN STUDENT s ON a.studentID = s.studentID
            WHERE a.internshipID = %s
        """, (internship_id,))
        applications = cursor.fetchall()

        return render_template(
            'view_applications.html',
            internship=internship,
            applications=applications
        )

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('company_dashboard'))

    finally:
        cursor.close()
        db_connection.close()

        
@app.route('/view_application_details/<int:application_id>', methods=['GET', 'POST'])
def view_application_details(application_id):
    # Ensure the user is logged in as a company
    if 'companyID' not in session:
        flash("You must be logged in as a company to view application details.", "error")
        return redirect(url_for('login'))

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'reset_pending':
                # Reset the application status to "Pending"
                cursor.execute("""
                    UPDATE APPLICATION
                    SET status = 'Pending'
                    WHERE applicationID = %s
                """, (application_id,))
                db_connection.commit()
                flash("The application status has been reverted to 'Pending'.", "success")

            # Handle other actions (e.g., accept, reject) as needed

            return redirect(url_for('view_application_details', application_id=application_id))

        cursor.execute("""
        SELECT a.applicationID, a.date, a.status, 
           s.fullName, s.email, s.phoneNumber, s.birthDate, s.resume, 
           i.title AS internshipTitle, i.internshipID, c.name AS companyName, s.studentID
        FROM APPLICATION a
        INNER JOIN STUDENT s ON a.studentID = s.studentID
        INNER JOIN INTERNSHIP i ON a.internshipID = i.internshipID
        INNER JOIN DEPARTMENT d ON i.departmentID = d.departmentID
        INNER JOIN COMPANY c ON d.companyID = c.companyID
        WHERE a.applicationID = %s
        """, (application_id,))
        application = cursor.fetchone()


        if not application:
            flash("Application not found.", "error")
            return redirect(url_for('company_dashboard'))

        # Fetch the student's major information
        cursor.execute("""
            SELECT sm.startDate, sm.graduationDate, sm.yearOfStudy, sm.CGPA, m.name AS majorName
            FROM STUDENT_MAJOR sm
            INNER JOIN MAJOR m ON sm.majorID = m.majorID
            WHERE sm.studentID = %s
        """, (application['studentID'],))
        major_info = cursor.fetchone()

        return render_template(
            'view_application_details.html',
            application=application,
            major_info=major_info
        )

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('company_dashboard'))

    finally:
        cursor.close()
        db_connection.close()



def email_exists(cursor, email):
    cursor.execute("SELECT COUNT(*) FROM USER WHERE email = %s", (email,))
    return cursor.fetchone()[0] > 0



def is_password_strong(password):
    # Password should have at least 8 characters, 1 uppercase, 1 lowercase, 1 digit, and 1 special character
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$'
    return bool(re.match(pattern, password))

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', 'resumes')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/resume/<int:student_id>')
def serve_resume(student_id):
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Fetch the resume filename for the student
        cursor.execute("SELECT resume FROM STUDENT WHERE studentID = %s", (student_id,))
        result = cursor.fetchone()

        if not result or not result['resume']:
            flash("No resume found for this student in the database.", "error")
            return redirect(url_for('company_dashboard'))

        # Construct the full file path
        resume_filename = result['resume']
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)

        # Debugging logs
        print(f"Resume filename from database: {resume_filename}")
        print(f"Full path to resume file: {resume_path}")
        print(f"Does file exist? {os.path.exists(resume_path)}")

        # Check if the file exists
        if not os.path.exists(resume_path):
            flash("The resume file is missing from the server.", "error")
            return redirect(url_for('company_dashboard'))

        # Serve the file
        return send_file(resume_path, as_attachment=False)

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('company_dashboard'))

    finally:
        cursor.close()
        db_connection.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
UPLOAD_FOLDER = 'uploads/resumes'

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Run the app on the local server
if __name__ == "__main__":
    app.run(debug=True)

