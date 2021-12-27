from flask import request, render_template, url_for, flash, redirect

from application import app, db
from application.models import AllDepartments, AllEmployees


# Home page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# Login user
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'secret':
            error = 'Invalid credential'
        else:
            flash('Welcome user')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


# All departments
@app.route('/departments')
def departments():
    """List all existing departments"""

    try:
        all_departments = AllDepartments.query.order_by(AllDepartments.id).all()
    except:
        return '<h1>Database query error<h1>', 500

    return render_template('departments.html',
                           all_departments=all_departments
                           )


# Generate specific department web-page
@app.route('/departments/<int:dep_id>')
def department(dep_id):
    """Create unique page with statistics for each department"""

    try:
        department_info = AllDepartments.query.get(dep_id)
        all_department_employees = AllEmployees.query.filter_by(department_id=dep_id)
    except:
        return "Database Query Error", 500
    return render_template('department.html',
                           department_info=department_info,
                           all_department_employees=all_department_employees
                           )


# ADD new department
@app.route('/departments/add-department', methods=['POST', 'GET'])
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
        except:
            return f'Error. Can not add new department to the database.'
    return render_template('add-department.html')


# UPDATE department info
@app.route('/departments/<int:dep_id>/update', methods=["POST", "GET"])
def update_department(dep_id):
    """Change department information"""

    title = 'Update Department'
    # Create object with new data
    department_info = AllDepartments.query.get(dep_id)
    if request.method == "POST":
        # Get new data from the update form
        department_info.dep_name = request.form['dep_name']
        # Push new object to the database
        try:
            db.session.commit()
            return redirect('/departments')
        except:
            return "<h2>Error while updating employee<2>"
    # If request method is GET => send data
    return render_template("update_department.html",
                           department_info=department_info,
                           title=title
                           )


# Delete department
@app.route('/departments/<int:id>/delete')
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
    except:
        return '<h2>Error. Cant delete department.<h2>' \
               '<h3>Transfer all employees to different department first</h3>'


# All company employees
@app.route('/employees')
def employees():
    """Query information about all existing employees from a db. List them on one page."""

    all_employees = AllEmployees.query.order_by(AllEmployees.name).all()
    return render_template('employees.html', all_employees=all_employees)


# Generate uniq page for each employee
@app.route('/employees/<int:emp_id>')
def employee(emp_id):
    """ Query employee data from a database, generate uniq page for each employee """

    employee_info = AllEmployees.query.get_or_404(emp_id)
    return render_template('employee.html',
                           emp_id=emp_id,
                           employee_info=employee_info
                           )


# ADD new employee to the database
@app.route('/employees/add-employee', methods=['POST', 'GET'])
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
        except:
            return '<h2>Error: Can not add new employee to the database<h2>'
    return render_template('add-employee.html',
                           all_departments=all_departments)


# UPDATE employee info
@app.route('/employees/<int:emp_id>/update', methods=["POST", "GET"])
def update_employee(emp_id):
    """Change employee information"""

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
        except:
            return "<h2>Error while updating employee<h2>"
    # If request method is GET => send page
    return render_template("update_employee.html",
                           employee_info=employee_info,
                           title=title
                           )


# DELETE employee from a database
@app.route('/employees/<int:id>/delete')
def delete_employee(id):
    # Chose the employee to delete from the db
    deleted = AllEmployees.query.get_or_404(id)
    try:
        db.session.delete(deleted)
        db.session.commit()
        return redirect('/employees')
    except:
        return 'Error. Cant delete employee.'
