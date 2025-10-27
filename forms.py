from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    status = SelectField('Status', choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')])
    deadline = DateTimeField('Deadline', format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Save')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('Developer', 'Developer'), ('Manager', 'Manager')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')