from flask import request, render_template, url_for, flash, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user

from application import app, db
from application.models import AllDepartments, AllEmployees, User


# Home page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title="Management App.")


# LOGIN user
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']

        # Check if length of the username and password exists and shorter than 32 and 225
        if len(username) <= 32 and len(password) <= 225:

            #  Check if User exits in the database
            user = User.query.filter_by(username=username).first()
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Welcome " + user.username)

                return redirect(url_for('index'))
            else:
                flash('Wrong credentials')
                return redirect(url_for('index'))
        else:
            error = 'Enter correct username and password'
            return render_template('error.html', error=error)
    return render_template('login.html',
                           error=error,
                           title="Log In")


# Logout user
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Handles user logout"""

    logout_user()
    return redirect(url_for('index'))


# Register new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration form

    username -- mandatory, up to 32 symbols
    password -- mandatory, will be hashed
    password2 -- mandatory, used only to check if a user entered desired password"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        # Check for empty fields in  form
        if not username or not password or not password2:
            flash("Please, fill all fields!")
            return redirect(url_for('register'))
        # Check if user retyped password correctly or made mistake typing desired password
        elif password != password2:
            return render_template('error.html', error="Password Retype Incorrect")
        else:
            # Hash password
            hash_pwd = generate_password_hash(password)
            # Create new user object
            new_user = User(username=username,
                            password=hash_pwd
                            )
            # Push new user object to the database
            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception:
                return render_template('error.html', error="Database error. User was now created")
            return redirect(url_for('login'))
    # Return registration form if request method is 'GET'
    return render_template('register.html',
                           title="Register new User"
                           )


# All departments
@app.route('/departments')
def departments():
    """List all existing departments"""

    try:
        all_departments = AllDepartments.query.order_by(AllDepartments.id).all()
    except Exception:
        return '<h1>Database query error<h1>', 500

    return render_template('departments.html',
                           all_departments=all_departments,
                           title="All Departments"
                           )


# Generate specific department web-page
@app.route('/departments/<int:dep_id>')
@login_required
def department(dep_id):
    """Create unique page with statistics and employees for each department"""

    try:
        department_info = AllDepartments.query.get(dep_id)
        department_name = department_info.dep_name
        all_department_employees = AllEmployees.query.filter_by(department_id=dep_id)
    except:
        return "Database Query Error", 500
    return render_template('department.html',
                           department_info=department_info,
                           all_department_employees=all_department_employees,
                           title=f"{department_name} Department"
                           )


# ADD new department
@app.route('/departments/add-department', methods=['POST', 'GET'])
@login_required
def add_department():
    """Add new department.

        Specify name for new department, ID will be assigned automatically.
    """

    if request.method == 'POST':
        dep_name = request.form['dep_name']

        # Create new object
        new_department = AllDepartments(dep_name=dep_name)
        # Save object to the database
        try:
            db.session.add(new_department)
            db.session.commit()
            return redirect(url_for('departments'))
        except Exception:
            return f'Error. Can not add new department to the database.'
    return render_template('add-department.html',
                           title="Add New Department")


# UPDATE department info
@app.route('/departments/<int:dep_id>/update', methods=["POST", "GET"])
@login_required
def update_department(dep_id):
    """Change department information"""

    # Create object with new data
    department_info = AllDepartments.query.get(dep_id)
    if request.method == "POST":
        # Get new data from the update form
        department_info.dep_name = request.form['dep_name']
        # Push new object to the database
        try:
            db.session.commit()
            return redirect('/departments')
        except Exception:
            return "<h2>Error while updating employee<2>"
    # If request method is GET => send data
    return render_template("update_department.html",
                           department_info=department_info,
                           title='Update Department'
                           )


# Delete department
@app.route('/departments/<int:id>/delete')
@login_required
def delete_department(id):
    """Chose the department to delete from the database by its ID.

        You have to transfer all employees to different department first.
        Be careful, deleting department is permanent.
    """

    deleted = AllDepartments.query.get_or_404(id)
    try:
        db.session.delete(deleted)
        db.session.commit()
        return redirect('/departments')
    except Exception:
        error='Error. Cant delete department.' \
               'Transfer all employees to different department first'
        return render_template("error.html", error=error)


# All company employees
@app.route('/employees')
def employees():
    """Query information about all existing employees from a db. List them on one page."""

    all_employees = AllEmployees.query.order_by(AllEmployees.name).all()
    return render_template('employees.html', all_employees=all_employees)


# Generate uniq page for each employee
@app.route('/employees/<int:emp_id>')
@login_required
def employee(emp_id):
    """ Query employee data from a database, generate uniq page for each employee """

    employee_info = AllEmployees.query.get_or_404(emp_id)
    return render_template('employee.html',
                           emp_id=emp_id,
                           employee_info=employee_info
                           )


# ADD new employee to the database
@app.route('/employees/add-employee', methods=['POST', 'GET'])
@login_required
def add_employee():
    """Create object 'new_employee' and push it to the database"""

    all_departments = AllDepartments.query.all()
    # Save input from the "add employee" form to variables
    if request.method == 'POST':
        department_id = request.form['department_id']
        salary = request.form['salary']
        name = request.form['name']
        lastname = request.form['lastname']

        # Create new object to add to the database
        new_employee = AllEmployees(
            department_id=department_id,
            salary=salary,
            name=name,
            lastname=lastname
        )

        # Push new_employee info to the database
        try:
            db.session.add(new_employee)
            db.session.commit()
            return redirect('/employees')
        except Exception:
            error = 'Error: Can not add new employee to the database'
            return render_template('error.html', error=error)
    return render_template('add-employee.html',
                           all_departments=all_departments)


# UPDATE employee info
@app.route('/employees/<int:emp_id>/update', methods=["POST", "GET"])
@login_required
def update_employee(emp_id):
    """Change employee information"""

    error = None
    title = "Update Employee info"
    # Create db object
    employee_info = AllEmployees.query.get(emp_id)
    if request.method == "POST":
        # Get data from the update form
        employee_info.department_id = request.form['department_id']
        employee_info.salary = request.form['salary']
        employee_info.name = request.form['name']
        employee_info.lastname = request.form['lastname']
        # Save object to db
        try:
            db.session.commit()
            return redirect('/employees')
        except Exception:
            error = "Error while updating employee"
            return render_template('error.html', error=error)
    # If request method is GET => send page
    return render_template("update_employee.html",
                           employee_info=employee_info,
                           title=title
                           )


# DELETE employee from a database
@app.route('/employees/<int:emp_id>/delete')
@login_required
def delete_employee(emp_id):
    error = None
    # Chose the employee to delete from the db
    deleted = AllEmployees.query.get_or_404(emp_id)
    try:
        db.session.delete(deleted)
        db.session.commit()
        return redirect('/employees')
    except Exception:
        error = "Error, user is not deleted"
        return render_template('error.html', error=error)
