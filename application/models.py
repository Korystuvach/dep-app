from flask_login import UserMixin
from datetime import date

from application import db, login_manager


# Create baseclass for employees table in db
class AllEmployees(db.Model):
    """Specify columns for all_employees table in the database.

    id -- unique value (will be generated automatically).
    department_id --  bind employee to department. Create department firs.
    salary -- Base salary. All bonuses will be calculated from this value.
    hire_date -- date today, generated automatically.
    """

    id = db.Column(db.Integer, primary_key=True)
    # Establish child relationship with departments table (id column)
    department_id = db.Column(db.Integer, db.ForeignKey('all_departments.id'), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(35), nullable=False)
    hire_date = db.Column(db.Date, default=date.today())

    def __repr__(self):
        return f"""
        id: {self.id}
        department_id: {self.department_id}
        salary: {self.salary}
        name: {self.name}
        lastname: {self.lastname}
        hire_date: {self.hire_date}
        """


# Create baseclass for departments table in db
class AllDepartments(db.Model):
    """Specify columns for all_departments table in the database

    id -- Department unique id, generated automatically
    dep_name -- Name of the department.
    """

    id = db.Column(db.Integer, primary_key=True)
    dep_name = db.Column(db.String(25), nullable=False, unique=True)
    # Establish relationship with employees / backref => create column for
    dep_employees_id = db.relationship('AllEmployees', backref='my_department', lazy=True)

    def __repr__(self):
        return f"""
        id: {self.id}
        dep_name: {self.dep_name}
        """


# Create User
class User(db.Model, UserMixin):
    """Handle application Users"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
