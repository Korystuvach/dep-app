"""This classes specify database structure

Classes:
    AllEmployees(db.Model)
    AllDepartments(db.Model)
    User(db.Model)

If any Changes are made to the classes, be sure
to perform database migration
"""

from flask_login import UserMixin
from datetime import date

from application import db, login_manager


# Create baseclass for employees table in db
class AllEmployees(db.Model):
    """Create all_employees table in the database.

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
    """Create table for all_departments  in the database

    id -- Department unique id, generated automatically
    dep_name -- Name of the department. required to create new department
    dep_employees_id -- connection with employees table
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


# Create User table
class User(db.Model, UserMixin):
    """Create table for application users. Handle User's authentication

    id -- unique user identifier. Generated automatically
    username -- credentials to log user in. Have to be unique value
    password -- secret word to identify user. Hashed.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    """Query User info from the database to handle login"""

    return User.query.get(user_id)
