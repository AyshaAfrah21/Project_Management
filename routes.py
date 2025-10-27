from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Project, Task
from forms import LoginForm, ProjectForm, TaskForm,SignupForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/')
@login_required
def dashboard():
    tasks = Task.query.filter_by(assigned_to=current_user.id).all() if current_user.role == 'Developer' else Task.query.all()
    overdue = [t for t in tasks if t.deadline and t.deadline < datetime.now()]
    metrics = {'total_tasks': len(tasks), 'overdue': len(overdue), 'progress': 50}  # Simple: Hardcoded to 50% for now
    return render_template('dashboard.html', metrics=metrics, tasks=tasks)

@main.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():
    if current_user.role not in ['Admin', 'Manager']:
        flash('Access denied')
        return redirect(url_for('main.dashboard'))
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data, manager_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash('Project created')
        return redirect(url_for('main.projects'))
    projects = Project.query.all()
    return render_template('projects.html', form=form, projects=projects)

@main.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data, status=form.status.data,
                    deadline=form.deadline.data, project_id=request.form.get('project_id'), assigned_to=request.form.get('assigned_to'))
        db.session.add(task)
        db.session.commit()
        flash('Task created')
        return redirect(url_for('main.tasks'))
    tasks = Task.query.filter_by(assigned_to=current_user.id).all() if current_user.role == 'Developer' else Task.query.all()
    projects = Project.query.all()
    users = User.query.all()
    return render_template('tasks.html', form=form, tasks=tasks, projects=projects, users=users)

@main.route('/admin')
@login_required
def admin():
    if current_user.role != 'Admin':
        flash('Access denied')
        return redirect(url_for('main.dashboard'))
    users = User.query.all()
    return render_template('admin.html', users=users)






@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists')
        else:
            hashed_pw = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=hashed_pw, role=form.role.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created! Please log in.')
            return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)