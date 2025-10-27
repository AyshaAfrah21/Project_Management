from flask import Blueprint, request
from ..extensions import db
from ..models import Task, Project, User
from ..schemas import TaskSchema
from flask_jwt_extended import jwt_required

tasks_bp = Blueprint('tasks', __name__)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    t = Task(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status','To Do'),
        deadline=data.get('deadline'),
        project_id=data['project_id'],
        assignee_id=data.get('assignee_id')
    )
    db.session.add(t)
    db.session.commit()
    return task_schema.dump(t), 201

@tasks_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def tasks_by_project(project_id):
    tasks = Task.query.filter_by(project_id=project_id).all()
    return tasks_schema.dump(tasks)

@tasks_bp.route('/<int:task_id>', methods=['PUT','DELETE'])
@jwt_required()
def modify_task(task_id):
    t = Task.query.get_or_404(task_id)
    if request.method == 'PUT':
        data = request.get_json()
        t.title = data.get('title', t.title)
        t.status = data.get('status', t.status)
        t.deadline = data.get('deadline', t.deadline)
        t.assignee_id = data.get('assignee_id', t.assignee_id)
        db.session.commit()
        return task_schema.dump(t)
    db.session.delete(t)
    db.session.commit()
    return {}, 204
